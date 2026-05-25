#!/usr/bin/env python3
"""LangSAM post-processing ablation on the 20-episode probe set.

For each episode:
  1. Read `lora_inference.json` (parsed.steps + affordance_hint + affordance UV).
  2. Run scripts/postprocess_affordance.refine_plan with GroundingDINO+SAM,
     using the source episode's rgb/depth/intrinsics from selection.json.
  3. Write `lora_inference_langsam.json` with step.affordance_refined per step.
  4. Compute per-episode UV MAE: raw-LoRA vs label, LangSAM-LoRA vs label.

Output:
  langsam_ablation.json    per-episode + aggregate numbers
  langsam_ablation.md      table for paper Section 4 ablation

Run (after run_experiment.py + score.py have run; can be at any time):
  CUDA_VISIBLE_DEVICES=0 \\
    /home/edge/miniconda3/envs/robobrain/bin/python \\
    /home/edge/RoboBrain/analysis_plan_quality/run_langsam_ablation.py
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import traceback
from pathlib import Path

PROJECT_ROOT = Path("/home/edge/RoboBrain/w50037733")
sys.path.insert(0, str(PROJECT_ROOT))

OUT_ROOT = Path("/home/edge/RoboBrain/analysis_plan_quality")
OUT_EP = OUT_ROOT / "episodes"


def uv_mae(pred_steps: list[dict], label_steps: list[dict], key: str = "affordance") -> float | None:
    pairs = []
    for ps, ls in zip(pred_steps, label_steps):
        pa = ps.get(key) if isinstance(ps, dict) else None
        la = ls.get("affordance") if isinstance(ls, dict) else None
        if isinstance(pa, list) and isinstance(la, list) and len(pa) >= 2 and len(la) >= 2:
            try:
                pairs.append(abs(float(pa[0]) - float(la[0])) + abs(float(pa[1]) - float(la[1])))
            except (TypeError, ValueError):
                pass
    if not pairs:
        return None
    return sum(pairs) / len(pairs) / 2.0


def fmt(v) -> str:
    if v is None:
        return "n/a"
    if isinstance(v, float):
        return f"{v:.3f}"
    return str(v)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tag", default="",
                        help="If set, reads lora_{tag}_inference.json and writes _{tag}_ outputs.")
    parser.add_argument("--selection", default="selection.json",
                        help="Selection file under analysis_plan_quality/ (e.g. selection_500.json).")
    args = parser.parse_args()
    in_name = f"lora_{args.tag}_inference.json" if args.tag else "lora_inference.json"
    out_name = f"lora_{args.tag}_inference_langsam.json" if args.tag else "lora_inference_langsam.json"
    suffix = f"_{args.tag}" if args.tag else ""

    import numpy as np
    from PIL import Image
    sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
    from postprocess_affordance import GroundingSAM, refine_plan

    sel = json.loads((OUT_ROOT / args.selection).read_text())
    print(f"Loaded {len(sel)} episodes from {args.selection}; input={in_name}")

    print("\n[GroundingSAM] loading models (one-time, ~1-2 min) ...", flush=True)
    t0 = time.time()
    grounder = GroundingSAM(device="cuda")
    print(f"  loaded in {time.time()-t0:.1f}s\n", flush=True)

    per_ep = []
    for s in sel:
        ep_dir = OUT_EP / f"{s['idx']:02d}_{s['dataset']}_{s['episode']}"
        ep_src = Path(s["path"])
        lora_path = ep_dir / in_name
        refined_path = ep_dir / "plan_v2_refined.json"

        if not lora_path.exists():
            print(f"  [{s['idx']:02d}] missing {in_name}, skip")
            continue

        out_path = ep_dir / out_name
        if out_path.exists():
            print(f"  [{s['idx']:02d}] {s['dataset']}/{s['episode']} cached")
            refined_lora = json.loads(out_path.read_text())
        else:
            try:
                rgb = Image.open(ep_src / "rgb_0.png").convert("RGB")
                depth_p = ep_src / "depth_0.npy"
                depth = np.load(depth_p) if depth_p.exists() else None
                meta_p = ep_src / "meta.json"
                if meta_p.exists():
                    K = np.array(json.loads(meta_p.read_text())["intrinsics"], dtype=np.float32)
                else:
                    # Fallback intrinsics — only used for 3D backproj which we don't score
                    K = np.array([[500, 0, 128], [0, 500, 128], [0, 0, 1]], dtype=np.float32)

                lora_doc = json.loads(lora_path.read_text())
                # refine_plan mutates plan dict in place; we want parsed.steps
                parsed = lora_doc.get("parsed") or {}
                # V2 LoRA emits `affordance_region` text but refine_plan reads
                # `affordance_hint` — copy across so the grounder works on V2 outputs.
                v2_steps = []
                for st in parsed.get("steps", []):
                    st = dict(st)
                    if not st.get("affordance_hint") and st.get("affordance_region"):
                        st["affordance_hint"] = st["affordance_region"]
                    v2_steps.append(st)
                plan_for_refine = {
                    "task": lora_doc.get("task", ""),
                    "scene_objects": parsed.get("scene_objects", []),
                    "steps": v2_steps,
                }
                t = time.time()
                refined_lora = refine_plan(rgb, depth, K, plan_for_refine, grounder, strategy="inscribed")
                out_path.write_text(json.dumps(refined_lora, indent=2, ensure_ascii=False))
                print(f"  [{s['idx']:02d}] {s['dataset']}/{s['episode']} {time.time()-t:.1f}s", flush=True)
            except Exception as e:
                print(f"  [{s['idx']:02d}] ERROR: {type(e).__name__}: {e}")
                traceback.print_exc()
                continue

        # Compute per-episode UV MAE: raw lora vs label, langsam vs label
        refined_label = json.loads(refined_path.read_text())
        label_steps = refined_label.get("steps", [])
        raw_steps = refined_lora.get("steps", [])

        mae_raw = uv_mae(raw_steps, label_steps, key="affordance")
        mae_lsam = uv_mae(raw_steps, label_steps, key="affordance_refined")
        n_ok = sum(1 for st in raw_steps if st.get("refine_status") == "ok")
        n_total = len(raw_steps)

        per_ep.append({
            "idx": s["idx"],
            "dataset": s["dataset"],
            "episode": s["episode"],
            "n_steps": n_total,
            "n_grounded_ok": n_ok,
            "grounding_success_rate": n_ok / n_total if n_total else None,
            "uv_mae_raw_vs_label": mae_raw,
            "uv_mae_langsam_vs_label": mae_lsam,
            "improvement": (mae_raw - mae_lsam) if (mae_raw is not None and mae_lsam is not None) else None,
        })

    # === Aggregate ===
    def mean(xs):
        xs = [x for x in xs if x is not None]
        return sum(xs) / len(xs) if xs else None

    agg = {
        "n_episodes": len(per_ep),
        "uv_mae_raw_vs_label": mean([e["uv_mae_raw_vs_label"] for e in per_ep]),
        "uv_mae_langsam_vs_label": mean([e["uv_mae_langsam_vs_label"] for e in per_ep]),
        "mean_improvement": mean([e["improvement"] for e in per_ep]),
        "grounding_success_rate": mean([e["grounding_success_rate"] for e in per_ep]),
    }

    (OUT_ROOT / f"langsam_ablation{suffix}.json").write_text(json.dumps(
        {"per_episode": per_ep, "aggregate": agg}, indent=2, ensure_ascii=False))

    # === Markdown report ===
    L = []
    L.append("# LangSAM Post-Processing Ablation\n")
    L.append(f"Episodes: **{agg['n_episodes']}** (same 20-ep set as scores.md)\n")
    L.append("## Aggregate")
    L.append(f"- **Raw LoRA UV MAE vs label:**    `{fmt(agg['uv_mae_raw_vs_label'])}`")
    L.append(f"- **LangSAM-refined UV MAE vs label:** `{fmt(agg['uv_mae_langsam_vs_label'])}`")
    L.append(f"- **Mean improvement (positive = LangSAM helps):** `{fmt(agg['mean_improvement'])}`")
    L.append(f"- **Grounding success rate** (steps where SAM returned a usable mask): `{fmt(agg['grounding_success_rate'])}`\n")

    L.append("## Per-episode")
    L.append("| # | Dataset | Episode | n_steps | grounded | UV MAE raw | UV MAE LangSAM | Δ (raw − LangSAM) |")
    L.append("|---|---|---|---|---|---|---|---|")
    for e in per_ep:
        L.append("| {idx:02d} | {ds} | {ep} | {n} | {g}/{n} | {r} | {l} | {d} |".format(
            idx=e["idx"], ds=e["dataset"], ep=e["episode"],
            n=e["n_steps"], g=e["n_grounded_ok"],
            r=fmt(e["uv_mae_raw_vs_label"]), l=fmt(e["uv_mae_langsam_vs_label"]),
            d=fmt(e["improvement"]),
        ))
    L.append("\n*Reading*: positive `Δ` means LangSAM moved the UV closer to the refined-label UV. "
             "Negative means LangSAM hurt. `grounded` = how many steps got a usable SAM mask "
             "(low rate → hint is too vague or object outside GroundingDINO's vocab).\n")

    (OUT_ROOT / f"langsam_ablation{suffix}.md").write_text("\n".join(L))
    print("\n=== AGGREGATE ===")
    for k, v in agg.items():
        print(f"  {k}: {fmt(v)}")
    print(f"\nWrote langsam_ablation{suffix}.json and langsam_ablation{suffix}.md")


if __name__ == "__main__":
    main()
