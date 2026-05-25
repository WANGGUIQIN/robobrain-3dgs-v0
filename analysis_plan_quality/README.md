# RoboBrain-3DGS — Plan-Quality Evaluation (A/B/C Probe)

Quantitative evaluation of the RoboBrain-3DGS planner. We score three plan
sources against the refined ground-truth (GT) label, per episode, across 7
manipulation datasets (RLBench / DROID / Bridge / RH20T / taco_play /
fractal20220817_data / jaco_play).

## The three systems under comparison

| Tag | System | Notes |
|-----|--------|-------|
| **A** | Base RoboBrain-3DGS (8B, no LoRA) | The ceiling without task-specific tuning. |
| **B** | GPT-v0 raw label | The upstream training label, scored against the refined GT. |
| **C** | **LoRA** (r=16, q/k/v/o), V2 plan format | The trained model. Scored both vs GT and vs Base. |

All three are scored against `plan_v2_refined.json` (the GT label).

## Two parallel research tracks (NOT versions)

- **V1 — ReKep path:** the VLM emits pixel `[u, v]` keypoints directly; a ReKep
  optimizer consumes them.
- **V2 — Lang-SAM path (this eval):** the VLM emits an `affordance_region`
  *text* description; GroundingDINO + SAM ground it to a pixel coordinate at
  runtime. The LM is never trained to regress coordinates — grounding is
  outsourced to Lang-SAM by design.

These are independent experiments. V1 checkpoints/data are kept separately and
are not part of this directory.

## Pipeline

```
rerun_inference_3epoch.py     # VLM → plan (raw V2 text, incl. affordance_region)
        │
run_langsam_ablation.py       # affordance_region text → GroundingDINO bbox → SAM mask → UV
        │
adapt_v2_to_v1.py             # map V2 fields (affordance_refined/_region) → V1 schema
        │
score.py                      # A/B/C metrics vs refined GT → metrics.json + scores.md
```

The Lang-SAM grounder lives in `w50037733/scripts/postprocess_affordance.py`
(not included here): GroundingDINO-base → SAM-ViT-large, with a target-noun
fallback at a relaxed box threshold.

## Headline results (20-episode probe, V2 LoRA epoch 3 + Lang-SAM)

Mean across episodes, scored vs refined GT. Full table in [`scores.md`](scores.md).

| Metric | LoRA (C) | Base (A) | GPT-v0 (B) | Δ LoRA vs Base |
|--------|----------|----------|------------|----------------|
| Action seq exact match | **0.700** | 0.500 | 1.000 | +20 pp |
| Action set Jaccard | **0.887** | 0.805 | 1.000 | +8 pp |
| Target Jaccard | **0.800** | 0.500 | 1.000 | +30 pp |
| Scene Jaccard | **0.660** | 0.563 | 1.000 | +10 pp |
| Affordance UV MAE | 0.176 | 0.162 | 0.000 | −8% (Lang-SAM ceiling) |
| [0.5,0.5] center-collapse rate | 0.000 | 0.000 | 0.000 | fix confirmed |
| Hint specificity (tokens) | **5.75** | 5.18 | 4.85 | +11% |
| Task-keyword preservation | **50%** | 17% | n/a | 3× |

Anchor findings:
- **rlbench**: LoRA EM 67% vs Base 0%; **taco_play**: LoRA EM 67% vs Base 0%.
- LoRA wins decisively on plan *structure* (actions, targets, scene); on UV it
  is bottlenecked by Lang-SAM grounding rather than by the LM — motivating the
  parallel V1 (direct-UV) track.

> A 500-episode expansion of this probe is in progress; the 20-episode reports
> here are final and the 500-episode reports will be added in a follow-up commit.

## File guide

| File | Contents |
|------|----------|
| `scores.md` / `metrics.json` | A/B/C aggregate + per-episode + per-dataset metrics |
| `langsam_ablation_planning_e{1,3}.{md,json}` | Lang-SAM grounding ablation, epoch 1 vs 3 |
| `selection.json` / `selection_500.json` | The 20- and 500-episode sampled sets (seeded) |
| `episodes/NN_<dataset>_<episode>/` | Per-episode plans + model outputs |
| &nbsp;&nbsp;`plan_v0_gpt.json` | Raw GPT label (B) |
| &nbsp;&nbsp;`plan_v2_refined.json` | Refined GT label |
| &nbsp;&nbsp;`base_inference.json` | Base model output (A) |
| &nbsp;&nbsp;`lora_*_inference.json` | LoRA raw output; `*_langsam.json` after grounding |
| &nbsp;&nbsp;`lora_inference.json` | LoRA adapted to V1 schema (what `score.py` reads as C) |

RGB frames (`rgb_0.png`) are symlinks into the local dataset and are
`.gitignore`d (they would be broken off-machine).

## Reproduce

```bash
# 1. inference (per checkpoint)
CUDA_VISIBLE_DEVICES=0 python rerun_inference_3epoch.py \
    --selection selection.json --base-mode --tag base
CUDA_VISIBLE_DEVICES=1 python rerun_inference_3epoch.py \
    --selection selection.json --ckpt <lora_ckpt> --tag planning_e3 --update-default
# 2. ground affordance_region → UV
python run_langsam_ablation.py --tag planning_e3 --selection selection.json
# 3. adapt + score
python adapt_v2_to_v1.py --tag planning_e3
python score.py
```
