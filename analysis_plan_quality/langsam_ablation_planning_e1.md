# LangSAM Post-Processing Ablation

Episodes: **20** (same 20-ep set as scores.md)

## Aggregate
- **Raw LoRA UV MAE vs label:**    `n/a`
- **LangSAM-refined UV MAE vs label:** `0.141`
- **Mean improvement (positive = LangSAM helps):** `n/a`
- **Grounding success rate** (steps where SAM returned a usable mask): `0.975`

## Per-episode
| # | Dataset | Episode | n_steps | grounded | UV MAE raw | UV MAE LangSAM | Δ (raw − LangSAM) |
|---|---|---|---|---|---|---|---|
| 01 | rlbench | episode_001722 | 3 | 3/3 | n/a | 0.310 | n/a |
| 02 | rlbench | episode_000236 | 5 | 5/5 | n/a | 0.147 | n/a |
| 03 | rlbench | episode_000052 | 4 | 4/4 | n/a | 0.120 | n/a |
| 04 | droid | episode_030298 | 4 | 2/4 | n/a | 0.280 | n/a |
| 05 | droid | episode_027110 | 4 | 4/4 | n/a | 0.108 | n/a |
| 06 | droid | episode_024947 | 4 | 4/4 | n/a | 0.119 | n/a |
| 07 | bridge | episode_004508 | 4 | 4/4 | n/a | 0.073 | n/a |
| 08 | bridge | episode_024406 | 4 | 4/4 | n/a | 0.096 | n/a |
| 09 | bridge | episode_003286 | 4 | 4/4 | n/a | 0.179 | n/a |
| 10 | rh20t | episode_003074 | 4 | 4/4 | n/a | 0.122 | n/a |
| 11 | rh20t | episode_003364 | 4 | 4/4 | n/a | 0.061 | n/a |
| 12 | rh20t | episode_002481 | 4 | 4/4 | n/a | 0.205 | n/a |
| 13 | taco_play | episode_000398 | 2 | 2/2 | n/a | 0.239 | n/a |
| 14 | taco_play | episode_002670 | 2 | 2/2 | n/a | 0.100 | n/a |
| 15 | taco_play | episode_001915 | 2 | 2/2 | n/a | 0.200 | n/a |
| 16 | fractal20220817_data | episode_005078 | 4 | 4/4 | n/a | 0.041 | n/a |
| 17 | fractal20220817_data | episode_004656 | 4 | 4/4 | n/a | 0.180 | n/a |
| 18 | jaco_play | episode_000103 | 4 | 4/4 | n/a | 0.138 | n/a |
| 19 | jaco_play | episode_000242 | 4 | 4/4 | n/a | 0.091 | n/a |
| 20 | jaco_play | episode_000260 | 2 | 2/2 | n/a | 0.020 | n/a |

*Reading*: positive `Δ` means LangSAM moved the UV closer to the refined-label UV. Negative means LangSAM hurt. `grounded` = how many steps got a usable SAM mask (low rate → hint is too vague or object outside GroundingDINO's vocab).
