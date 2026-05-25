# A/B/C Plan-Quality Quantitative Scores

Episodes: **20** across 7 datasets (RLBench/DROID/Bridge/rh20t/taco_play/fractal/jaco_play)

## Headline aggregate (mean across episodes)

| Metric | LoRA vs Refined | Base vs Refined | GPT-v0 vs Refined | LoRA vs Base |
|---|---|---|---|---|
| Action seq exact match | 0.700 | 0.500 | 1.000 | 0.550 |
| Action set Jaccard | 0.887 | 0.805 | 1.000 | 0.838 |
| Mean |step count diff| | 0.300 | 0.650 | 0.000 | 0.650 |
| Target Jaccard | 0.800 | 0.500 | 1.000 | 0.425 |
| Scene Jaccard | 0.660 | 0.563 | 1.000 | 0.511 |
| Affordance UV MAE | 0.176 | 0.162 | 0.000 | 0.217 |
| [0.5,0.5] center rate | 0.000 | 0.000 | 0.000 | 0.000 |
| Hint tokens (mean) | 5.754 | 5.183 | 4.854 | 5.754 |
| Has release rate | 0.000 | 0.100 | 0.100 | 0.000 |

## Task-keyword preservation (direction terms like 'right'/'open' showing up in pred)
- **lora_vs_refined**: 6/12 (50%) of episodes with directional task keywords
- **base_vs_refined**: 2/12 (17%) of episodes with directional task keywords

## Per-episode action exact match
| # | Dataset/episode | Task | LoRA EM | Base EM | LoRA steps | Refined steps |
|---|---|---|---|---|---|---|
| 01 | rlbench_episode_001722 | turn right tap | 1 | 0 | 3 | 3 |
| 02 | rlbench_episode_000236 | screw in the gray light bulb | 1 | 0 | 4 | 4 |
| 03 | rlbench_episode_000052 | close the olive jar | 0 | 0 | 4 | 4 |
| 04 | droid_episode_030298 | Put the paper bag on the counter | 1 | 1 | 4 | 4 |
| 05 | droid_episode_027110 | Pick up the black cup from the stove and | 1 | 1 | 4 | 4 |
| 06 | droid_episode_024947 | Remove the black glove from near the key | 1 | 1 | 4 | 4 |
| 07 | bridge_episode_004508 | Take the white wedge out of the bowl and | 1 | 1 | 4 | 4 |
| 08 | bridge_episode_024406 | Place the drumstick on top of the green  | 1 | 1 | 4 | 4 |
| 09 | bridge_episode_003286 | pick orange toy from vessel and keep it  | 1 | 1 | 4 | 4 |
| 10 | rh20t_episode_003074 | Assemble: Attach the bubble ring to the  | 0 | 0 | 3 | 4 |
| 11 | rh20t_episode_003364 | Insert the pencil into the pencil sharpe | 1 | 0 | 4 | 4 |
| 12 | rh20t_episode_002481 | Assemble one piece of a puzzle | 0 | 1 | 3 | 4 |
| 13 | taco_play_episode_000398 | pick up the yellow block | 1 | 0 | 2 | 2 |
| 14 | taco_play_episode_002670 | push the pink block inside the drawer | 0 | 0 | 2 | 3 |
| 15 | taco_play_episode_001915 | go towards the yellow block and lift it | 1 | 0 | 3 | 3 |
| 16 | fractal20220817_data_episode_005078 | place blue plastic bottle into top drawe | 1 | 1 | 4 | 4 |
| 17 | fractal20220817_data_episode_004656 | move blue plastic bottle near green can | 1 | 1 | 4 | 4 |
| 18 | jaco_play_episode_000103 | place the yellow cup in the dish rack | 1 | 1 | 4 | 4 |
| 19 | jaco_play_episode_000242 | pick up the milk dairy | 0 | 0 | 4 | 3 |
| 20 | jaco_play_episode_000260 | pick up the apple fruit | 0 | 0 | 4 | 2 |

## Per-dataset breakdown
LoRA vs Refined / Base vs Refined, grouped by source dataset.
| Dataset | n | LoRA EM | Base EM | LoRA UV MAE | Base UV MAE | LoRA step-diff | Base step-diff | LoRA hint-tok | Base hint-tok |
|---|---|---|---|---|---|---|---|---|---|
| bridge | 3 | 1.000 | 1.000 | 0.148 | 0.110 | 0.000 | 0.000 | 6.250 | 4.833 |
| droid | 3 | 1.000 | 1.000 | 0.263 | 0.213 | 0.000 | 0.000 | 6.167 | 4.583 |
| fractal20220817_data | 2 | 1.000 | 1.000 | 0.110 | 0.107 | 0.000 | 0.000 | 7.750 | 7.250 |
| jaco_play | 3 | 0.333 | 0.333 | 0.173 | 0.149 | 1.000 | 1.000 | 6.583 | 5.750 |
| rh20t | 3 | 0.333 | 0.333 | 0.125 | 0.122 | 0.667 | 0.333 | 5.444 | 4.983 |
| rlbench | 3 | 0.667 | 0.000 | 0.208 | 0.164 | 0.000 | 2.000 | 5.750 | 5.238 |
| taco_play | 3 | 0.667 | 0.000 | 0.180 | 0.249 | 0.333 | 1.000 | 3.000 | 4.333 |

*Reading this table*: a dataset where LoRA EM ≫ Base EM is one where LoRA learned the training distribution well. A dataset where LoRA step-diff is large (e.g. taco_play) is one where LoRA over-predicts step count — likely a dataset-specific training-label bias rather than a model weakness.


## What to read in this table
- **Action seq EM**: did the pred reproduce the exact ordered action list? High LoRA EM + low Base EM → LoRA learned the training distribution.
- **Affordance UV MAE**: 0 means pred matches label exactly; ~0.25 means roughly random in the unit square. **If `[0.5,0.5] center rate` is high, LoRA collapsed to predicting the image center — i.e., the pointing head did NOT learn.**
- **Hint specificity**: refined label hints have ~5–8 tokens; raw GPT and untrained model produce ~2–3 tokens ('the X'). LoRA close to refined → it learned to copy hints; far → underfit on hint refinement.
- **Has release rate**: training labels often omit release. If LoRA matches that omission rate, it inherited the GPT label bias.