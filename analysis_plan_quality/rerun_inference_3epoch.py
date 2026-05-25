#!/usr/bin/env python3
"""Re-run inference on the 20-episode probe set using the 3-epoch LoRA checkpoint.

Reads selection.json (the 20 episodes locked in by run_experiment.py's seeded
sample) and writes a new `lora_3epoch_inference.json` per episode. Existing
`lora_inference.json` files (sanity 1-epoch outputs) are first renamed to
`lora_1epoch_inference.json` so score.py picks up the latest checkpoint by
default — but the 1-epoch results stay on disk for the sanity-vs-3epoch
delta table.

Run (after 3-epoch training completes):
  CUDA_VISIBLE_DEVICES=0 \\
    /home/edge/miniconda3/envs/robobrain/bin/python \\
    /home/edge/RoboBrain/analysis_plan_quality/rerun_inference_3epoch.py
"""
from __future__ import annotations

import argparse
import contextlib
import io
import json
import sys
import time
import traceback
from pathlib import Path

PROJECT_ROOT = Path("/home/edge/RoboBrain/w50037733")
sys.path.insert(0, str(PROJECT_ROOT))

OUT_ROOT = Path("/home/edge/RoboBrain/analysis_plan_quality")
OUT_EP = OUT_ROOT / "episodes"

MODEL_PATH = "/home/edge/RoboBrain/models/RoboBrain2.5-8B-NV"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ckpt", default="/home/edge/RoboBrain/outputs/lora_3epoch/best",
                        help="LoRA checkpoint directory to evaluate. Use NONE for base model.")
    parser.add_argument("--tag", default="3epoch",
                        help="Output filename tag → {tag}_inference.json (or lora_{tag}_inference.json).")
    parser.add_argument("--update-default", action="store_true",
                        help="Also overwrite lora_inference.json so score.py picks this up by default.")
    parser.add_argument("--selection", default="selection.json",
                        help="Selection file under analysis_plan_quality/ (e.g. selection_500.json).")
    parser.add_argument("--base-mode", action="store_true",
                        help="If set, ignore --ckpt and run base model (no LoRA). Writes base_inference.json.")
    args = parser.parse_args()

    sel_file = OUT_ROOT / args.selection
    if not sel_file.exists():
        print(f"ERROR: {sel_file} missing.", file=sys.stderr)
        sys.exit(1)

    if not args.base_mode and not Path(args.ckpt).exists():
        print(f"ERROR: checkpoint not found at {args.ckpt}.", file=sys.stderr)
        sys.exit(1)

    selection = json.loads(sel_file.read_text())
    print(f"Loaded {len(selection)} episodes from {args.selection}")

    if args.base_mode:
        out_name = "base_inference.json"
    else:
        out_name = f"lora_{args.tag}_inference.json"

    from inference_3dgs import UnifiedInference3DGS
    from utils.prompt_utils import parse_planning_output

    if args.base_mode:
        print(f"\n[base] loading base model (no LoRA) ...", flush=True)
        t0 = time.time()
        model = UnifiedInference3DGS(model_id=MODEL_PATH, checkpoint=None, mode="lora")
    else:
        print(f"\n[{args.tag}] loading model from ckpt={args.ckpt} ...", flush=True)
        t0 = time.time()
        model = UnifiedInference3DGS(
            model_id=MODEL_PATH,
            checkpoint=args.ckpt,
            mode="lora",
        )
    print(f"  loaded in {time.time()-t0:.1f}s", flush=True)

    for s in selection:
        ep_dir = OUT_EP / f"{s['idx']:02d}_{s['dataset']}_{s['episode']}"
        ep_src = Path(s["path"])
        out_tagged = ep_dir / out_name
        out_default = ep_dir / "lora_inference.json"

        if out_tagged.exists():
            print(f"  [{s['idx']:02d}] {s['dataset']}/{s['episode']} cached", flush=True)
            continue

        plan = json.loads((ep_src / "plan.json").read_text())
        task_str = plan.get("task", "manipulation")

        t = time.time()
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                result = model.inference(
                    text=task_str,
                    image=str(ep_src / "rgb_0.png"),
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
            payload = {"task": task_str, "ckpt": args.ckpt, "raw": answer, "parsed": parsed_plan}
        except Exception as e:
            payload = {
                "task": task_str,
                "ckpt": args.ckpt,
                "error": f"{type(e).__name__}: {e}",
                "traceback": traceback.format_exc(),
            }

        out_tagged.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
        if args.update_default:
            out_default.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
        print(f"  [{s['idx']:02d}] {s['dataset']}/{s['episode']} {time.time()-t:.1f}s", flush=True)

    del model
    import torch
    torch.cuda.empty_cache()
    print(f"\n[{args.tag}] done. Output: lora_{args.tag}_inference.json per episode.")


if __name__ == "__main__":
    main()
