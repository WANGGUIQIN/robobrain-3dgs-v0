#!/usr/bin/env python3
"""Sample 500 episodes for the expanded A/B/C probe.

Keeps the existing 20 (idx 1-20) and adds 480 new ones, balanced ~71/dataset.
Writes selection_500.json with the merged list. Also copies plan files into
new per-episode dirs under episodes/.
"""
from __future__ import annotations

import json
import random
import shutil
from pathlib import Path

PROJECT_ROOT = Path("/home/edge/RoboBrain/w50037733")
DATA_ROOT = PROJECT_ROOT / "data" / "processed"
OUT_ROOT = Path("/home/edge/RoboBrain/analysis_plan_quality")
OUT_EP = OUT_ROOT / "episodes"

TARGET_TOTAL = 500
SEED = 7
PER_DATASET_NEW = {
    "rlbench": 69,
    "droid": 69,
    "bridge": 69,
    "rh20t": 69,
    "taco_play": 69,
    "jaco_play": 69,
    "fractal20220817_data": 66,
}
# 20 existing + 480 new = 500


def main() -> None:
    random.seed(SEED)
    existing = json.loads((OUT_ROOT / "selection.json").read_text())
    print(f"Existing selection: {len(existing)} episodes")
    used = {(e["dataset"], e["episode"]) for e in existing}

    new_entries: list[dict] = []
    next_idx = max(e["idx"] for e in existing) + 1
    for ds, n_new in PER_DATASET_NEW.items():
        ds_dir = DATA_ROOT / ds
        if not ds_dir.exists():
            print(f"  skip {ds}: not found")
            continue
        candidates = [
            e for e in sorted(ds_dir.iterdir())
            if e.is_dir() and e.name.startswith("episode_")
            and (e / "rgb_0.png").exists() and (e / "plan.json").exists()
            and (ds, e.name) not in used
        ]
        if len(candidates) < n_new:
            print(f"  WARN {ds}: only {len(candidates)} candidates, requested {n_new}")
        sample = random.sample(candidates, min(n_new, len(candidates)))
        for p in sample:
            new_entries.append({
                "idx": next_idx,
                "dataset": ds,
                "episode": p.name,
                "path": str(p),
            })
            next_idx += 1
        print(f"  {ds}: added {len(sample)} (total avail {len(candidates)})")

    merged = existing + new_entries
    (OUT_ROOT / "selection_500.json").write_text(
        json.dumps(merged, indent=2, ensure_ascii=False))
    print(f"\nMerged: {len(merged)} episodes (existing {len(existing)} + new {len(new_entries)})")

    # === Build episode dirs for new entries ===
    print("\nCopying plans into new episode dirs ...")
    n_done = 0
    for e in new_entries:
        out_dir = OUT_EP / f"{e['idx']:02d}_{e['dataset']}_{e['episode']}"
        out_dir.mkdir(parents=True, exist_ok=True)
        src = Path(e["path"])
        # symlink image (large) but copy plans (small, edited downstream)
        rgb_dst = out_dir / "rgb_0.png"
        if not rgb_dst.exists():
            rgb_dst.symlink_to(src / "rgb_0.png")
        # plan.json -> plan_v2_refined.json (training label = "refined")
        shutil.copy2(src / "plan.json", out_dir / "plan_v2_refined.json")
        # plan_v0.json -> plan_v0_gpt.json (raw GPT label)
        gpt_src = src / "plan_v0.json"
        if gpt_src.exists():
            shutil.copy2(gpt_src, out_dir / "plan_v0_gpt.json")
        n_done += 1
    print(f"  setup {n_done} new episode dirs")


if __name__ == "__main__":
    main()
