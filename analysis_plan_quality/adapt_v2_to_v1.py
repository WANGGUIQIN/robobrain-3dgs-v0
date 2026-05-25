#!/usr/bin/env python3
"""Adapt V2 LoRA + LangSAM output to V1 schema for score.py.

Reads lora_{tag}_inference_langsam.json from each episode dir, and writes
lora_inference.json with the V2 fields mapped to V1 schema:

  step.affordance_refined (LangSAM UV)   ->  step.affordance
  step.affordance_region  (V2 LoRA text) ->  step.affordance_hint

Run:
  python adapt_v2_to_v1.py --tag planning_e3
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path("/home/edge/RoboBrain/analysis_plan_quality")
EP_ROOT = ROOT / "episodes"


def adapt_steps(steps: list[dict]) -> list[dict]:
    out = []
    for s in steps:
        s = dict(s)
        if s.get("affordance_refined") and not s.get("affordance"):
            s["affordance"] = s["affordance_refined"]
        if s.get("affordance_region") and not s.get("affordance_hint"):
            s["affordance_hint"] = s["affordance_region"]
        out.append(s)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", required=True,
                    help="Reads lora_{tag}_inference_langsam.json per episode.")
    args = ap.parse_args()

    in_name = f"lora_{args.tag}_inference_langsam.json"
    n_done = n_missing = 0
    for ep_dir in sorted(EP_ROOT.iterdir()):
        if not ep_dir.is_dir():
            continue
        src = ep_dir / in_name
        if not src.exists():
            n_missing += 1
            continue
        # Load the langsam output (just steps inside; matches refine_plan output structure)
        langsam = json.loads(src.read_text())
        steps = adapt_steps(langsam.get("steps", []))
        # Build a doc that score.py can consume (mirrors inference output shape)
        out = {
            "task": langsam.get("task", ""),
            "parsed": {
                "scene_objects": langsam.get("scene_objects", []),
                "steps": steps,
            },
        }
        (ep_dir / "lora_inference.json").write_text(
            json.dumps(out, indent=2, ensure_ascii=False))
        n_done += 1
    print(f"adapted {n_done} episodes, missing {n_missing}")


if __name__ == "__main__":
    main()
