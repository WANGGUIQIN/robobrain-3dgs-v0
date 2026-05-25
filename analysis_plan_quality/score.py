#!/usr/bin/env python3
"""Quantitative scorer for the A/B/C plan-quality probe.

Inputs (per episode dir under analysis_plan_quality/episodes/<NN>_<ds>_<ep>/):
  plan_v0_gpt.json       raw GPT-4o-mini label (upstream training source)
  plan_v2_refined.json   refined training label (hints rewritten by RoboBrain)
  base_inference.json    base RoboBrain output (no LoRA)
  lora_inference.json    LoRA checkpoint output

Computes per-episode + aggregate metrics. Writes:
  analysis_plan_quality/metrics.json   per-episode numeric details
  analysis_plan_quality/scores.md      human-readable report

Metrics (each computed for LoRA-vs-Refined and Base-vs-Refined):
  - action_seq_em      exact match on the ordered action list
  - action_set_jaccard set IoU on action multiset
  - step_count_diff    |pred_steps - label_steps|
  - target_jaccard     set IoU on per-step targets
  - scene_jaccard      set IoU on scene_objects
  - affordance_uv_mae  mean abs error on [u,v] for aligned step indices
  - affordance_at_center_rate  fraction of pred steps with affordance ≈ [0.5,0.5]
  - hint_specificity   mean tokens in affordance_hint (proxy for "the X" vs "the handle of the X")
  - has_release        bool: last step's action == "release"
  - task_in_destination  bool: rotate/move steps' destination string contains a task keyword

Run:
  python /home/edge/RoboBrain/analysis_plan_quality/score.py
"""
from __future__ import annotations

import json
import math
from collections import Counter
from pathlib import Path

ROOT = Path("/home/edge/RoboBrain/analysis_plan_quality")
EP_ROOT = ROOT / "episodes"


def load_steps(payload: dict) -> tuple[list[str], list[dict], list[str]]:
    """Return (scene_objects, steps_list, action_list).

    Handles both label-style (top-level {steps,scene_objects}) and
    inference-style ({task, raw, parsed:{steps,scene_objects}}).
    """
    if "parsed" in payload:
        body = payload.get("parsed") or {}
    else:
        body = payload
    scene = body.get("scene_objects") or []
    steps = body.get("steps") or []
    if not isinstance(steps, list):
        steps = []
    actions = [str(s.get("action", "")).strip().lower() for s in steps if isinstance(s, dict)]
    return scene, steps, actions


def jaccard(a: list, b: list) -> float:
    sa, sb = set(map(str, a)), set(map(str, b))
    if not sa and not sb:
        return 1.0
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)


def affordance_uv_mae(pred_steps: list[dict], label_steps: list[dict]) -> float | None:
    """Mean abs UV error on aligned step indices (truncate to shorter)."""
    pairs = []
    for ps, ls in zip(pred_steps, label_steps):
        pa = ps.get("affordance") if isinstance(ps, dict) else None
        la = ls.get("affordance") if isinstance(ls, dict) else None
        if isinstance(pa, list) and isinstance(la, list) and len(pa) >= 2 and len(la) >= 2:
            try:
                pairs.append(abs(float(pa[0]) - float(la[0])) + abs(float(pa[1]) - float(la[1])))
            except (TypeError, ValueError):
                pass
    if not pairs:
        return None
    return sum(pairs) / len(pairs) / 2.0  # avg per coordinate


def at_center_rate(pred_steps: list[dict]) -> float | None:
    if not pred_steps:
        return None
    hits = 0
    n = 0
    for s in pred_steps:
        a = s.get("affordance") if isinstance(s, dict) else None
        if isinstance(a, list) and len(a) >= 2:
            n += 1
            try:
                if abs(float(a[0]) - 0.5) < 1e-3 and abs(float(a[1]) - 0.5) < 1e-3:
                    hits += 1
            except (TypeError, ValueError):
                pass
    if n == 0:
        return None
    return hits / n


def hint_specificity(steps: list[dict]) -> float | None:
    """Avg token count of affordance_hint across steps (excludes 'the X' generic = 2 tokens)."""
    counts = []
    for s in steps:
        h = (s.get("affordance_hint") or "").strip() if isinstance(s, dict) else ""
        if h:
            counts.append(len(h.split()))
    if not counts:
        return None
    return sum(counts) / len(counts)


def targets(steps: list[dict]) -> list[str]:
    out = []
    for s in steps:
        if isinstance(s, dict):
            t = s.get("target")
            if t is not None:
                out.append(str(t).strip().lower())
    return out


def has_release(actions: list[str]) -> bool:
    return any("release" in a or "let_go" in a for a in actions)


def task_keyword_in_destination(pred_steps: list[dict], task: str) -> bool | None:
    """Did the pred preserve a task keyword (e.g., 'right' in 'turn right tap') in destination/target?"""
    task_lower = (task or "").lower()
    keywords = [w for w in ["left", "right", "up", "down", "top", "bottom",
                            "front", "back", "open", "close"] if w in task_lower]
    if not keywords:
        return None
    for s in pred_steps:
        if not isinstance(s, dict):
            continue
        blob = " ".join(str(s.get(k, "")) for k in ("target", "destination", "done_when"))
        if any(kw in blob.lower() for kw in keywords):
            return True
    return False


def score_pred_vs_label(pred: dict, label: dict) -> dict:
    p_scene, p_steps, p_actions = load_steps(pred)
    l_scene, l_steps, l_actions = load_steps(label)
    task = pred.get("task") or label.get("task") or ""
    return {
        "action_seq_em": int(p_actions == l_actions),
        "action_set_jaccard": jaccard(p_actions, l_actions),
        "step_count_diff": abs(len(p_steps) - len(l_steps)),
        "pred_step_count": len(p_steps),
        "label_step_count": len(l_steps),
        "target_jaccard": jaccard(targets(p_steps), targets(l_steps)),
        "scene_jaccard": jaccard(p_scene, l_scene),
        "affordance_uv_mae": affordance_uv_mae(p_steps, l_steps),
        "at_center_rate": at_center_rate(p_steps),
        "hint_specificity": hint_specificity(p_steps),
        "has_release": has_release(p_actions),
        "task_in_destination": task_keyword_in_destination(p_steps, task),
    }


def score_episode(ep_dir: Path) -> dict:
    files = {
        "gpt": ep_dir / "plan_v0_gpt.json",
        "refined": ep_dir / "plan_v2_refined.json",
        "base": ep_dir / "base_inference.json",
        "lora": ep_dir / "lora_inference.json",
    }
    data = {k: json.loads(p.read_text()) if p.exists() else None for k, p in files.items()}
    refined = data["refined"]
    out = {"episode": ep_dir.name, "task": (refined or {}).get("task", "?")}
    if data["lora"] is not None and refined is not None:
        out["lora_vs_refined"] = score_pred_vs_label(data["lora"], refined)
    if data["base"] is not None and refined is not None:
        out["base_vs_refined"] = score_pred_vs_label(data["base"], refined)
    if data["gpt"] is not None and refined is not None:
        out["gpt_vs_refined"] = score_pred_vs_label(data["gpt"], refined)
    if data["lora"] is not None and data["base"] is not None:
        out["lora_vs_base"] = score_pred_vs_label(data["lora"], data["base"])
    return out


def _mean(xs: list[float]) -> float | None:
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs) if xs else None


def aggregate(per_ep: list[dict], comparison: str) -> dict:
    """Aggregate one comparison family (e.g., 'lora_vs_refined') across episodes."""
    pulled = [e[comparison] for e in per_ep if comparison in e]
    if not pulled:
        return {}
    return {
        "n": len(pulled),
        "action_seq_em_rate": _mean([p["action_seq_em"] for p in pulled]),
        "action_set_jaccard": _mean([p["action_set_jaccard"] for p in pulled]),
        "step_count_diff_mean": _mean([p["step_count_diff"] for p in pulled]),
        "target_jaccard": _mean([p["target_jaccard"] for p in pulled]),
        "scene_jaccard": _mean([p["scene_jaccard"] for p in pulled]),
        "affordance_uv_mae": _mean([p["affordance_uv_mae"] for p in pulled]),
        "at_center_rate": _mean([p["at_center_rate"] for p in pulled]),
        "hint_specificity": _mean([p["hint_specificity"] for p in pulled]),
        "has_release_rate": _mean([float(p["has_release"]) for p in pulled]),
    }


def parse_dataset(ep_name: str) -> str:
    """'01_rlbench_episode_001722' -> 'rlbench'; handles 'fractal20220817_data' too."""
    head = ep_name.rsplit("_episode_", 1)[0]
    parts = head.split("_", 1)
    return parts[1] if len(parts) == 2 and parts[0].isdigit() else head


def per_dataset_aggregate(per_ep: list[dict], comparison: str) -> dict[str, dict]:
    """Group per-episode results by dataset name, aggregate each."""
    by_ds: dict[str, list[dict]] = {}
    for e in per_ep:
        ds = parse_dataset(e["episode"])
        by_ds.setdefault(ds, []).append(e)
    return {ds: aggregate(eps, comparison) for ds, eps in by_ds.items()}


def task_in_dest_summary(per_ep: list[dict], comparison: str) -> tuple[int, int]:
    """Returns (preserved, applicable) — episodes where task keyword applies."""
    preserved = applicable = 0
    for e in per_ep:
        if comparison not in e:
            continue
        v = e[comparison].get("task_in_destination")
        if v is None:
            continue
        applicable += 1
        if v:
            preserved += 1
    return preserved, applicable


def fmt(v) -> str:
    if v is None:
        return "n/a"
    if isinstance(v, float):
        return f"{v:.3f}"
    return str(v)


def main() -> None:
    ep_dirs = sorted([d for d in EP_ROOT.iterdir() if d.is_dir()])
    print(f"Scoring {len(ep_dirs)} episodes ...", flush=True)
    per_ep = [score_episode(d) for d in ep_dirs]

    metrics = {
        "per_episode": per_ep,
        "aggregate": {
            "lora_vs_refined": aggregate(per_ep, "lora_vs_refined"),
            "base_vs_refined": aggregate(per_ep, "base_vs_refined"),
            "gpt_vs_refined": aggregate(per_ep, "gpt_vs_refined"),
            "lora_vs_base": aggregate(per_ep, "lora_vs_base"),
        },
        "per_dataset": {
            "lora_vs_refined": per_dataset_aggregate(per_ep, "lora_vs_refined"),
            "base_vs_refined": per_dataset_aggregate(per_ep, "base_vs_refined"),
        },
        "task_keyword_preserved": {
            "lora_vs_refined": task_in_dest_summary(per_ep, "lora_vs_refined"),
            "base_vs_refined": task_in_dest_summary(per_ep, "base_vs_refined"),
        },
    }
    (ROOT / "metrics.json").write_text(json.dumps(metrics, indent=2, ensure_ascii=False))

    # === Markdown report ===
    L = []
    L.append("# A/B/C Plan-Quality Quantitative Scores\n")
    L.append(f"Episodes: **{len(per_ep)}** across 7 datasets (RLBench/DROID/Bridge/rh20t/taco_play/fractal/jaco_play)\n")
    L.append("## Headline aggregate (mean across episodes)\n")
    L.append("| Metric | LoRA vs Refined | Base vs Refined | GPT-v0 vs Refined | LoRA vs Base |")
    L.append("|---|---|---|---|---|")
    keys = [
        ("action_seq_em_rate", "Action seq exact match"),
        ("action_set_jaccard", "Action set Jaccard"),
        ("step_count_diff_mean", "Mean |step count diff|"),
        ("target_jaccard", "Target Jaccard"),
        ("scene_jaccard", "Scene Jaccard"),
        ("affordance_uv_mae", "Affordance UV MAE"),
        ("at_center_rate", "[0.5,0.5] center rate"),
        ("hint_specificity", "Hint tokens (mean)"),
        ("has_release_rate", "Has release rate"),
    ]
    for k, label in keys:
        row = [label]
        for cmp in ("lora_vs_refined", "base_vs_refined", "gpt_vs_refined", "lora_vs_base"):
            row.append(fmt(metrics["aggregate"].get(cmp, {}).get(k)))
        L.append("| " + " | ".join(row) + " |")
    L.append("")

    # Task keyword preservation
    L.append("## Task-keyword preservation (direction terms like 'right'/'open' showing up in pred)")
    for cmp in ("lora_vs_refined", "base_vs_refined"):
        p, a = metrics["task_keyword_preserved"][cmp]
        rate = f"{p}/{a}" + (f" ({100*p/a:.0f}%)" if a > 0 else "")
        L.append(f"- **{cmp}**: {rate} of episodes with directional task keywords")
    L.append("")

    # Per-episode small table
    L.append("## Per-episode action exact match")
    L.append("| # | Dataset/episode | Task | LoRA EM | Base EM | LoRA steps | Refined steps |")
    L.append("|---|---|---|---|---|---|---|")
    for e in per_ep:
        lvr = e.get("lora_vs_refined", {})
        bvr = e.get("base_vs_refined", {})
        L.append("| {ep} | {ep2} | {task} | {lem} | {bem} | {lc} | {rc} |".format(
            ep=e["episode"].split("_")[0],
            ep2="_".join(e["episode"].split("_")[1:]),
            task=str(e["task"])[:40].replace("|", "/"),
            lem=fmt(lvr.get("action_seq_em")),
            bem=fmt(bvr.get("action_seq_em")),
            lc=fmt(lvr.get("pred_step_count")),
            rc=fmt(lvr.get("label_step_count")),
        ))

    # Per-dataset breakdown
    L.append("\n## Per-dataset breakdown")
    L.append("LoRA vs Refined / Base vs Refined, grouped by source dataset.")
    L.append("| Dataset | n | LoRA EM | Base EM | LoRA UV MAE | Base UV MAE | LoRA step-diff | Base step-diff | LoRA hint-tok | Base hint-tok |")
    L.append("|---|---|---|---|---|---|---|---|---|---|")
    lvr_ds = metrics["per_dataset"]["lora_vs_refined"]
    bvr_ds = metrics["per_dataset"]["base_vs_refined"]
    for ds in sorted(lvr_ds.keys()):
        a = lvr_ds[ds]
        b = bvr_ds.get(ds, {})
        L.append("| {ds} | {n} | {l_em} | {b_em} | {l_uv} | {b_uv} | {l_sd} | {b_sd} | {l_ht} | {b_ht} |".format(
            ds=ds, n=a.get("n", 0),
            l_em=fmt(a.get("action_seq_em_rate")), b_em=fmt(b.get("action_seq_em_rate")),
            l_uv=fmt(a.get("affordance_uv_mae")),  b_uv=fmt(b.get("affordance_uv_mae")),
            l_sd=fmt(a.get("step_count_diff_mean")), b_sd=fmt(b.get("step_count_diff_mean")),
            l_ht=fmt(a.get("hint_specificity")),   b_ht=fmt(b.get("hint_specificity")),
        ))
    L.append("\n*Reading this table*: a dataset where LoRA EM ≫ Base EM is one where LoRA "
             "learned the training distribution well. A dataset where LoRA step-diff is large "
             "(e.g. taco_play) is one where LoRA over-predicts step count — likely a "
             "dataset-specific training-label bias rather than a model weakness.\n")

    L.append("\n## What to read in this table")
    L.append("- **Action seq EM**: did the pred reproduce the exact ordered action list? "
             "High LoRA EM + low Base EM → LoRA learned the training distribution.")
    L.append("- **Affordance UV MAE**: 0 means pred matches label exactly; ~0.25 means roughly random in the unit square. "
             "**If `[0.5,0.5] center rate` is high, LoRA collapsed to predicting the image center — i.e., the pointing head did NOT learn.**")
    L.append("- **Hint specificity**: refined label hints have ~5–8 tokens; raw GPT and untrained model produce ~2–3 tokens ('the X'). "
             "LoRA close to refined → it learned to copy hints; far → underfit on hint refinement.")
    L.append("- **Has release rate**: training labels often omit release. If LoRA matches that omission rate, "
             "it inherited the GPT label bias.")

    (ROOT / "scores.md").write_text("\n".join(L))
    print(f"Wrote {ROOT/'metrics.json'} and {ROOT/'scores.md'}", flush=True)

    # Brief stdout summary
    agg = metrics["aggregate"]
    print("\n=== AGGREGATE SUMMARY ===")
    for cmp in ("lora_vs_refined", "base_vs_refined", "gpt_vs_refined"):
        a = agg.get(cmp, {})
        print(f"  {cmp:24s}  action_EM={fmt(a.get('action_seq_em_rate'))}  "
              f"target_J={fmt(a.get('target_jaccard'))}  "
              f"uv_MAE={fmt(a.get('affordance_uv_mae'))}  "
              f"center_rate={fmt(a.get('at_center_rate'))}  "
              f"hint_tok={fmt(a.get('hint_specificity'))}  "
              f"has_release={fmt(a.get('has_release_rate'))}")


if __name__ == "__main__":
    main()
