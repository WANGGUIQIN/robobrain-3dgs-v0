#!/usr/bin/env python3
"""A/B/C plan-quality probe (see PAPER_PLAN.md §"语义拆解不合理"诊断).

Layout produced under analysis_plan_quality/episodes/<NN>_<dataset>_<ep>/:
  rgb_0.png              scene image (binary copy, not a symlink)
  plan_v0_gpt.json       Stage B   — raw GPT-4o-mini output (training label upstream source)
  plan_v2_refined.json   Stage B   — current training label (hints refined by RoboBrain)
  base_inference.json    Stage C   — base RoboBrain (no LoRA) output on same image+task
  lora_inference.json    Stage A   — LoRA checkpoint output on same image+task

Plus a top-level summary.md with side-by-side diffs and quick aggregate stats.

Run:
  CUDA_VISIBLE_DEVICES=0 \
    /home/edge/miniconda3/envs/robobrain/bin/python \
    /home/edge/RoboBrain/analysis_plan_quality/run_experiment.py
"""
from __future__ import annotations

import contextlib
import io
import json
import random
import shutil
import sys
import time
import traceback
from pathlib import Path

PROJECT_ROOT = Path("/home/edge/RoboBrain/w50037733")
sys.path.insert(0, str(PROJECT_ROOT))

OUT_ROOT = Path("/home/edge/RoboBrain/analysis_plan_quality")
OUT_EP = OUT_ROOT / "episodes"
DATA_ROOT = PROJECT_ROOT / "data" / "processed"

MODEL_PATH = "/home/edge/RoboBrain/models/RoboBrain2.5-8B-NV"
LORA_CKPT = "/home/edge/RoboBrain/outputs/lora_sanity/checkpoint-13319"

# 20 episodes spread over 7 datasets so we see schema drift, not just one source.
N_PER_DATASET = {
    "rlbench": 3,
    "droid": 3,
    "bridge": 3,
    "rh20t": 3,
    "taco_play": 3,
    "fractal20220817_data": 2,
    "jaco_play": 3,
}
SEED = 42


def pick_episodes() -> list[tuple[str, Path]]:
    """Return (dataset_name, episode_dir) pairs that have both rgb_0.png and plan.json."""
    random.seed(SEED)
    picked: list[tuple[str, Path]] = []
    for ds, n in N_PER_DATASET.items():
        ds_dir = DATA_ROOT / ds
        if not ds_dir.exists():
            print(f"  skip {ds}: not found", flush=True)
            continue
        candidates = [
            e for e in sorted(ds_dir.iterdir())
            if e.is_dir() and e.name.startswith("episode_")
            and (e / "rgb_0.png").exists() and (e / "plan.json").exists()
        ]
        if not candidates:
            print(f"  skip {ds}: 0 valid episodes", flush=True)
            continue
        sample = random.sample(candidates, min(n, len(candidates)))
        picked.extend((ds, p) for p in sample)
    return picked


def stage_B_copy_plans(episodes: list[tuple[str, Path]]) -> None:
    """Copy raw GPT plan + refined plan + image into per-episode subdirs."""
    print(f"\n[Stage B] copying plans for {len(episodes)} episodes ...", flush=True)
    for i, (ds, ep) in enumerate(episodes, 1):
        out = OUT_EP / f"{i:02d}_{ds}_{ep.name}"
        out.mkdir(parents=True, exist_ok=True)
        # Image
        shutil.copy2(ep / "rgb_0.png", out / "rgb_0.png")
        # Refined plan = current training label
        shutil.copy2(ep / "plan.json", out / "plan_v2_refined.json")
        # Raw GPT plan = plan_v0.json if hint-refinement happened, else current plan
        gpt_src = ep / "plan_v0.json"
        if gpt_src.exists():
            shutil.copy2(gpt_src, out / "plan_v0_gpt.json")
        else:
            # No v0 means episode was never refined — current plan IS the GPT one.
            # Mark it so the analyst knows.
            data = json.loads((ep / "plan.json").read_text())
            data["__note__"] = "Episode was never hint-refined; this IS the GPT-4o-mini output."
            (out / "plan_v0_gpt.json").write_text(json.dumps(data, indent=2, ensure_ascii=False))
        print(f"  [{i:02d}/{len(episodes)}] {ds}/{ep.name}", flush=True)


def run_inference_pass(episodes: list[tuple[str, Path]], ckpt: str | None, tag: str) -> None:
    """Load model once, run on all episodes, save <tag>_inference.json per episode."""
    from inference_3dgs import UnifiedInference3DGS
    from utils.prompt_utils import parse_planning_output

    print(f"\n[Stage {tag}] loading model ckpt={ckpt or 'NONE (base)'} ...", flush=True)
    t0 = time.time()
    model = UnifiedInference3DGS(
        model_id=MODEL_PATH,
        checkpoint=ckpt,
        mode="lora",
    )
    print(f"  loaded in {time.time()-t0:.1f}s", flush=True)

    for i, (ds, ep) in enumerate(episodes, 1):
        out_dir = OUT_EP / f"{i:02d}_{ds}_{ep.name}"
        out_file = out_dir / f"{tag}_inference.json"
        if out_file.exists():
            print(f"  [{i:02d}/{len(episodes)}] {ds}/{ep.name} cached", flush=True)
            continue

        plan = json.loads((ep / "plan.json").read_text())
        task_str = plan.get("task", "manipulation")

        t = time.time()
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                result = model.inference(
                    text=task_str,
                    image=str(ep / "rgb_0.png"),
                    task="planning",
                    do_sample=False,
                    temperature=0.0,
                    max_new_tokens=1024,
                )
            answer = result.get("answer", "")
            try:
                parsed_plan = parse_planning_output(answer)
            except Exception as pe:
                parsed_plan = {"parse_error": f"{type(pe).__name__}: {pe}"}
            payload = {
                "task": task_str,
                "raw": answer,
                "parsed": parsed_plan,
            }
        except Exception as e:
            payload = {
                "task": task_str,
                "error": f"{type(e).__name__}: {e}",
                "traceback": traceback.format_exc(),
            }
        out_file.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
        print(f"  [{i:02d}/{len(episodes)}] {ds}/{ep.name} {time.time()-t:.1f}s", flush=True)

    del model
    import torch
    torch.cuda.empty_cache()
    print(f"[Stage {tag}] done.", flush=True)


def write_summary(episodes: list[tuple[str, Path]]) -> None:
    """Aggregate counts + per-episode side-by-side into summary.md."""
    print("\n[summary] writing summary.md ...", flush=True)
    lines: list[str] = []
    lines.append("# Plan-Quality A/B/C Experiment\n")
    lines.append(f"- Episodes: **{len(episodes)}**")
    lines.append(f"- LoRA ckpt: `{LORA_CKPT}`")
    lines.append(f"- Base model: `{MODEL_PATH}`\n")
    lines.append("## What each file contains")
    lines.append("| File | Source | What to look for |")
    lines.append("|------|--------|------------------|")
    lines.append("| `plan_v0_gpt.json`     | GPT-4o-mini (the upstream training label) | Hallucinated objects, bad action sequencing — if **GPT** is wrong, training inherits the error. |")
    lines.append("| `plan_v2_refined.json` | Same as above, but `affordance_hint` rewritten by RoboBrain | Only hints change; actions/targets/constraints unchanged. |")
    lines.append("| `base_inference.json`  | Base RoboBrain (no LoRA) on the same image+task | The 'ceiling' — if base is bad, LoRA can't fix it.|")
    lines.append("| `lora_inference.json`  | LoRA checkpoint-13319 on the same image+task | The trained model's actual output. Compare with GPT label to see what LoRA learned.|")

    lines.append("\n## How to read the comparison")
    lines.append("- **A** = compare `lora_inference.json` vs `plan_v2_refined.json` (training-set memorization vs underfit)")
    lines.append("- **B** = inspect `plan_v0_gpt.json` (was the GPT label itself reasonable?)")
    lines.append("- **C** = compare `base_inference.json` vs `lora_inference.json` (did LoRA improve or degrade over base?)")
    lines.append("")

    # Aggregate quick numbers
    bad_lora = bad_base = err_lora = err_base = 0
    rows = []
    for i, (ds, ep) in enumerate(episodes, 1):
        d = OUT_EP / f"{i:02d}_{ds}_{ep.name}"

        def _summ(fp: Path) -> str:
            if not fp.exists():
                return "MISSING"
            try:
                j = json.loads(fp.read_text())
            except Exception as e:
                return f"PARSE_ERR:{e}"
            if "error" in j:
                return f"ERR: {j['error'][:80]}"
            raw = (j.get("raw") or "")[:140].replace("\n", " ↵ ")
            return raw + ("…" if len(j.get("raw") or "") > 140 else "")

        lora = _summ(d / "lora_inference.json")
        base = _summ(d / "base_inference.json")
        if "ERR" in lora:
            err_lora += 1
        if "ERR" in base:
            err_base += 1

        gpt_plan = json.loads((d / "plan_v0_gpt.json").read_text())
        task = gpt_plan.get("task", "?")
        n_steps = len(gpt_plan.get("steps", []))
        rows.append((f"{i:02d}", ds, ep.name, task, n_steps))

    lines.append(f"## Quick stats")
    lines.append(f"- LoRA inference errors: **{err_lora}/{len(episodes)}**")
    lines.append(f"- Base inference errors: **{err_base}/{len(episodes)}**\n")

    lines.append("## Episode index")
    lines.append("| # | Dataset | Episode | Task (truncated) | GPT steps |")
    lines.append("|---|---------|---------|------------------|-----------|")
    for r in rows:
        task_short = r[3][:60].replace("|", "/")
        lines.append(f"| {r[0]} | {r[1]} | {r[2]} | {task_short} | {r[4]} |")

    (OUT_ROOT / "summary.md").write_text("\n".join(lines))
    print("  done.", flush=True)


def main() -> None:
    OUT_EP.mkdir(parents=True, exist_ok=True)
    episodes = pick_episodes()
    print(f"Selected {len(episodes)} episodes across {len(set(e[0] for e in episodes))} datasets.")

    # Persist the selection so re-runs (or the user inspecting) see the same list
    (OUT_ROOT / "selection.json").write_text(json.dumps(
        [{"idx": i, "dataset": ds, "episode": ep.name, "path": str(ep)}
         for i, (ds, ep) in enumerate(episodes, 1)],
        indent=2,
    ))

    stage_B_copy_plans(episodes)
    run_inference_pass(episodes, ckpt=None, tag="base")          # Stage C
    run_inference_pass(episodes, ckpt=LORA_CKPT, tag="lora")     # Stage A
    write_summary(episodes)
    print("\nAll done. See:", OUT_ROOT, flush=True)


if __name__ == "__main__":
    main()
