# A/B/C Plan-Quality Quantitative Scores

Episodes: **500** across 7 datasets (RLBench/DROID/Bridge/rh20t/taco_play/fractal/jaco_play)

## Headline aggregate (mean across episodes)

| Metric | LoRA vs Refined | Base vs Refined | GPT-v0 vs Refined | LoRA vs Base |
|---|---|---|---|---|
| Action seq exact match | 0.710 | 0.492 | 1.000 | 0.562 |
| Action set Jaccard | 0.887 | 0.769 | 1.000 | 0.799 |
| Mean |step count diff| | 0.300 | 0.702 | 0.000 | 0.674 |
| Target Jaccard | 0.784 | 0.550 | 1.000 | 0.510 |
| Scene Jaccard | 0.662 | 0.308 | 1.000 | 0.308 |
| Affordance UV MAE | 0.165 | 0.162 | 0.000 | 0.217 |
| [0.5,0.5] center rate | 0.000 | 0.000 | 0.004 | 0.000 |
| Hint tokens (mean) | 5.959 | 5.183 | 4.849 | 5.959 |
| Has release rate | 0.026 | 0.088 | 0.066 | 0.026 |

## Task-keyword preservation (direction terms like 'right'/'open' showing up in pred)
- **lora_vs_refined**: 124/230 (54%) of episodes with directional task keywords
- **base_vs_refined**: 89/230 (39%) of episodes with directional task keywords

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
| 100 | droid_episode_055228 | Put the lid of the silver thing on the t | 1 | 1 | 4 | 4 |
| 101 | droid_episode_018440 | Fold the tissue paper in half | 0 | 0 | 4 | 3 |
| 102 | droid_episode_037652 | Pick up the light blue cloth peg and put | 1 | 1 | 4 | 4 |
| 103 | droid_episode_016825 | Move the package from left to right. | 1 | 1 | 4 | 4 |
| 104 | droid_episode_074730 | Move the pineapple plushie to the right | 0 | 1 | 3 | 4 |
| 105 | droid_episode_056126 | Pick the black pen on the table and put  | 1 | 0 | 4 | 4 |
| 106 | droid_episode_004456 | Place the silver spoon in the glass cont | 0 | 0 | 6 | 4 |
| 107 | droid_episode_008674 | Pick up the scoop and put it in the obje | 1 | 1 | 4 | 4 |
| 108 | droid_episode_034609 | Put one of the left towels on the counte | 1 | 1 | 4 | 4 |
| 109 | droid_episode_037483 | Move the foil paper on the counter | 1 | 1 | 4 | 4 |
| 10 | rh20t_episode_003074 | Assemble: Attach the bubble ring to the  | 0 | 0 | 3 | 4 |
| 110 | droid_episode_038541 | Move the pan to the top right corner of  | 1 | 1 | 4 | 4 |
| 111 | droid_episode_077222 | Put the wrench in the bowl | 1 | 1 | 4 | 4 |
| 112 | droid_episode_065708 | Clean the plate with the towel and move  | 0 | 0 | 4 | 4 |
| 113 | droid_episode_007644 | Press the button on the top right side o | 1 | 0 | 2 | 2 |
| 114 | droid_episode_010343 | Place the white towel on the tripod. | 1 | 1 | 4 | 4 |
| 115 | droid_episode_029789 | Put one marble on the window seal | 1 | 1 | 4 | 4 |
| 116 | droid_episode_070918 | Close the trash can lid. | 1 | 1 | 3 | 3 |
| 117 | droid_episode_007227 | Turn the object on the arm of the sofa t | 0 | 0 | 4 | 3 |
| 118 | droid_episode_006760 | Remove the glue stick from the open draw | 1 | 1 | 4 | 4 |
| 119 | droid_episode_034218 | Turn the faucet to the right | 1 | 1 | 3 | 3 |
| 11 | rh20t_episode_003364 | Insert the pencil into the pencil sharpe | 1 | 0 | 4 | 4 |
| 120 | droid_episode_062800 | Put the cups into each other in the blac | 0 | 0 | 12 | 6 |
| 121 | droid_episode_031360 | Move the green pot to the right, open th | 0 | 0 | 8 | 11 |
| 122 | droid_episode_046112 | Put the blue block on the orange plate | 1 | 1 | 4 | 4 |
| 123 | droid_episode_038282 | Use the object to mix the contents in th | 0 | 0 | 3 | 4 |
| 124 | droid_episode_002586 | Put the the purple plushie in the box | 1 | 1 | 4 | 4 |
| 125 | droid_episode_067536 | Open the top of the grill | 0 | 0 | 3 | 3 |
| 126 | droid_episode_039149 | Pick up the green cup, place it on the b | 0 | 1 | 6 | 8 |
| 127 | droid_episode_018806 | Move the silver object from the storage  | 1 | 1 | 4 | 4 |
| 128 | droid_episode_012901 | Pick up the toy egg and put it in the or | 1 | 1 | 4 | 4 |
| 129 | droid_episode_076358 | Move the brown bowl forward slightly | 1 | 0 | 3 | 3 |
| 12 | rh20t_episode_002481 | Assemble one piece of a puzzle | 0 | 1 | 3 | 4 |
| 130 | droid_episode_006572 | Open the first drawer under the fruit pl | 0 | 0 | 3 | 3 |
| 131 | droid_episode_024404 | Pick up the bottle from the base top and | 1 | 1 | 4 | 4 |
| 132 | droid_episode_031677 | Move the empty plastic pack of snack for | 0 | 0 | 4 | 3 |
| 133 | droid_episode_014268 | Rotate the silver stand on the right. | 1 | 1 | 3 | 3 |
| 134 | droid_episode_027386 | Put the scoop inside the blue cup and th | 0 | 0 | 5 | 5 |
| 135 | droid_episode_049473 | Move the lid to the table | 1 | 1 | 4 | 4 |
| 136 | droid_episode_047247 | Move the green block to the right side o | 1 | 1 | 4 | 4 |
| 137 | droid_episode_077193 | Take the black pen out of the clear cup  | 1 | 0 | 4 | 4 |
| 138 | droid_episode_009033 | Scatter the objects in the stack, and th | 0 | 0 | 4 | 5 |
| 139 | droid_episode_018597 | Pick the orange block from the table and | 1 | 1 | 4 | 4 |
| 13 | taco_play_episode_000398 | pick up the yellow block | 1 | 0 | 2 | 2 |
| 140 | droid_episode_063728 | Put the orange can in the open cabinet. | 1 | 1 | 4 | 4 |
| 141 | droid_episode_050792 | Use the wooden spoon to mix inside the p | 0 | 0 | 4 | 4 |
| 142 | droid_episode_030625 | Move the green eraser to the right | 1 | 1 | 4 | 4 |
| 143 | droid_episode_015060 | Take the blue cup out of the orange cup  | 1 | 0 | 4 | 4 |
| 144 | droid_episode_058569 | Put the white cable in the storage box | 1 | 0 | 4 | 4 |
| 145 | droid_episode_030667 | Fold the grey thing in half | 0 | 0 | 4 | 4 |
| 146 | droid_episode_054360 | Pick up one object and put it on the tab | 1 | 1 | 4 | 4 |
| 147 | droid_episode_039548 | Put the lid on the towels | 1 | 1 | 4 | 4 |
| 148 | droid_episode_044402 | Pick up the wipe and clean the top of th | 1 | 0 | 4 | 4 |
| 149 | droid_episode_025613 | Move the white mug backwards | 1 | 0 | 3 | 3 |
| 14 | taco_play_episode_002670 | push the pink block inside the drawer | 0 | 0 | 2 | 3 |
| 150 | droid_episode_016687 | Put the dark bule object in the sink | 1 | 1 | 4 | 4 |
| 151 | droid_episode_009262 | Move the green block on top of the cabin | 1 | 1 | 4 | 4 |
| 152 | droid_episode_019708 | Move the white mug from the right to the | 1 | 0 | 4 | 4 |
| 153 | droid_episode_016734 | Put the white piece of clothing on the s | 1 | 1 | 4 | 4 |
| 154 | droid_episode_025706 | Uncover the pot | 1 | 0 | 4 | 4 |
| 155 | droid_episode_025831 | Remove the bottle from the pot and put i | 1 | 1 | 4 | 4 |
| 156 | droid_episode_001415 | Remove the bowl from the cupboard | 1 | 1 | 4 | 4 |
| 157 | droid_episode_073625 | Uncover the container | 0 | 0 | 4 | 3 |
| 158 | droid_episode_020442 | Remove the book from the bowl and put it | 1 | 1 | 4 | 4 |
| 159 | bridge_episode_008710 | place pot on green foam. pot placed on f | 1 | 1 | 4 | 4 |
| 15 | taco_play_episode_001915 | go towards the yellow block and lift it | 1 | 0 | 3 | 3 |
| 160 | bridge_episode_009445 | Move the pot to the bottom middle of sto | 1 | 1 | 4 | 4 |
| 161 | bridge_episode_000082 | Move the chocolate from the pan to the l | 1 | 1 | 4 | 4 |
| 162 | bridge_episode_004706 | Place the red item towards the top left  | 1 | 1 | 4 | 4 |
| 163 | bridge_episode_013927 | Move potato to middle front of stove top | 1 | 1 | 4 | 4 |
| 164 | bridge_episode_017729 | Put the spatula under the sushi. | 1 | 1 | 4 | 4 |
| 165 | bridge_episode_012287 | Move cloth to left edge of table in fron | 1 | 1 | 4 | 4 |
| 166 | bridge_episode_020116 | put pepper in pot or pan | 1 | 1 | 4 | 4 |
| 167 | bridge_episode_018789 | Place the white and black vegetable to t | 1 | 1 | 4 | 4 |
| 168 | bridge_episode_010662 | Move the red pepper to the right of the  | 1 | 1 | 4 | 4 |
| 169 | bridge_episode_004013 | move grapes to the back left corner of s | 1 | 1 | 4 | 4 |
| 16 | fractal20220817_data_episode_005078 | place blue plastic bottle into top drawe | 1 | 1 | 4 | 4 |
| 170 | bridge_episode_022853 | Place red potato inside of silver bowl. | 1 | 0 | 4 | 4 |
| 171 | bridge_episode_017102 | Scoot the pot to the counter's far left  | 1 | 0 | 3 | 3 |
| 172 | bridge_episode_020391 | Put the cucumber in the pot. | 1 | 1 | 4 | 4 |
| 173 | bridge_episode_021665 | move potato to below spoon | 1 | 1 | 4 | 4 |
| 174 | bridge_episode_022380 | Place cucumber at diagonal angle at bott | 1 | 1 | 4 | 4 |
| 175 | bridge_episode_024537 | Move the yellow cloth behind the pot wit | 1 | 0 | 4 | 4 |
| 176 | bridge_episode_001654 | pick upthe yellow towel put on the anoth | 1 | 1 | 4 | 4 |
| 177 | bridge_episode_015041 | Move the banana to the top right of the  | 1 | 1 | 4 | 4 |
| 178 | bridge_episode_022560 | Place the red and white vegetable to the | 1 | 1 | 4 | 4 |
| 179 | bridge_episode_018536 | move the pot to the towel | 1 | 1 | 4 | 4 |
| 17 | fractal20220817_data_episode_004656 | move blue plastic bottle near green can | 1 | 1 | 4 | 4 |
| 180 | bridge_episode_013128 | move metal pot to right lower corner | 1 | 1 | 4 | 4 |
| 181 | bridge_episode_013315 | Slide the silver pot in front of the can | 0 | 0 | 4 | 3 |
| 182 | bridge_episode_013343 | Move the bluye cloth close to the silver | 1 | 1 | 4 | 4 |
| 183 | bridge_episode_013185 | Move the silver pot forward to the empty | 1 | 1 | 4 | 4 |
| 184 | bridge_episode_003318 | flip cup upright | 0 | 0 | 4 | 3 |
| 185 | bridge_episode_015958 | Take the green object and put it on the  | 1 | 1 | 4 | 4 |
| 186 | bridge_episode_020943 | Place the metal bowl behind the orange t | 1 | 1 | 4 | 4 |
| 187 | bridge_episode_013393 | Pick up the blueberries and place them o | 1 | 1 | 4 | 4 |
| 188 | bridge_episode_001887 | Pick up the potato and place it on the y | 1 | 1 | 4 | 4 |
| 189 | bridge_episode_006249 | Place the red spoon inside the orange po | 1 | 0 | 4 | 4 |
| 18 | jaco_play_episode_000103 | place the yellow cup in the dish rack | 1 | 1 | 4 | 4 |
| 190 | bridge_episode_002062 | Move the green napkin from left end to r | 1 | 1 | 4 | 4 |
| 191 | bridge_episode_006881 | Take the carrot from the silver vessel a | 0 | 1 | 4 | 4 |
| 192 | bridge_episode_014580 | Move the towel below the microwave | 1 | 1 | 4 | 4 |
| 193 | bridge_episode_005230 | Place the spoon in front of the can. | 1 | 1 | 4 | 4 |
| 194 | bridge_episode_003536 | place blue cloth next to yellow knife | 1 | 0 | 4 | 4 |
| 195 | bridge_episode_011336 | close cabinet | 1 | 0 | 2 | 2 |
| 196 | bridge_episode_019785 | Move the towel to right of spoon but mid | 1 | 1 | 4 | 4 |
| 197 | bridge_episode_001600 | Move bowl from the towel to the left sid | 1 | 1 | 4 | 4 |
| 198 | bridge_episode_003284 | Move the blue spoon next to the silver p | 1 | 1 | 4 | 4 |
| 199 | bridge_episode_000004 | Move the kadai and place it at the right | 1 | 1 | 4 | 4 |
| 19 | jaco_play_episode_000242 | pick up the milk dairy | 0 | 0 | 4 | 3 |
| 200 | bridge_episode_018797 | pick up green mug | 0 | 0 | 2 | 3 |
| 201 | bridge_episode_004862 | Place croissant inside of silver pot. | 1 | 1 | 4 | 4 |
| 202 | bridge_episode_017796 | Put the cheese into the pot. | 1 | 1 | 4 | 4 |
| 203 | bridge_episode_003252 | Place the orange on the green cloth. | 1 | 1 | 4 | 4 |
| 204 | bridge_episode_012082 | bring the orange to the front edge from  | 1 | 1 | 4 | 4 |
| 205 | bridge_episode_020254 | place the brush at the left side of the  | 0 | 1 | 0 | 4 |
| 206 | bridge_episode_000787 | Place the blue cloth between the pot and | 1 | 0 | 4 | 4 |
| 207 | bridge_episode_002147 | move the black and white object to the o | 1 | 1 | 4 | 4 |
| 208 | bridge_episode_006844 | move blue fork to lower right corner | 1 | 1 | 4 | 4 |
| 209 | bridge_episode_020273 | Place eggplant to the right of the chick | 1 | 0 | 4 | 4 |
| 20 | jaco_play_episode_000260 | pick up the apple fruit | 0 | 0 | 4 | 2 |
| 210 | bridge_episode_012585 | Put the hotdog to the left of the spoon. | 1 | 1 | 4 | 4 |
| 211 | bridge_episode_004787 | Move the blue fork and place it on the y | 1 | 1 | 4 | 4 |
| 212 | bridge_episode_020948 | Move the egg from the back of the table  | 1 | 1 | 4 | 4 |
| 213 | bridge_episode_008405 | Move the spatula from the back to the si | 1 | 1 | 4 | 4 |
| 214 | bridge_episode_011557 | Put the spoon to the right of the cloth. | 1 | 1 | 4 | 4 |
| 215 | bridge_episode_019848 | Move the green cloth to the right of the | 1 | 1 | 4 | 4 |
| 216 | bridge_episode_012097 | Pick up the spoon and drop it at the bot | 1 | 0 | 4 | 4 |
| 217 | bridge_episode_015702 | Move the blue cloth to the back left cor | 1 | 1 | 4 | 4 |
| 218 | bridge_episode_003924 | Put the napkin more towards the top of t | 0 | 0 | 4 | 3 |
| 219 | bridge_episode_003710 | (These pictures aren't working) | 0 | 0 | 1 | 4 |
| 21 | rlbench_episode_000713 | stack the wine bottle to the left of the | 1 | 1 | 4 | 4 |
| 220 | bridge_episode_016172 | move croissant to above towel | 1 | 1 | 4 | 4 |
| 221 | bridge_episode_015413 | Place the pot immediately to the left of | 1 | 1 | 4 | 4 |
| 222 | bridge_episode_015923 | put spatula in pan | 1 | 1 | 4 | 4 |
| 223 | bridge_episode_016014 | Lift the toy potato sitting in the silve | 1 | 1 | 4 | 4 |
| 224 | bridge_episode_010441 | Move the yellow scrubber to the front le | 1 | 1 | 4 | 4 |
| 225 | bridge_episode_002687 | Move the fish to the left of the green t | 1 | 1 | 4 | 4 |
| 226 | bridge_episode_004671 | Place red ring on the left edge | 1 | 1 | 4 | 4 |
| 227 | bridge_episode_003276 | Place red utensil above the yellow cloth | 1 | 1 | 4 | 4 |
| 228 | rh20t_episode_003409 | Plug in the power cord to the socket | 1 | 0 | 4 | 4 |
| 229 | rh20t_episode_001561 | Screw the lid onto the jar | 0 | 0 | 4 | 4 |
| 22 | rlbench_episode_000321 | take the chicken off the grill | 1 | 1 | 4 | 4 |
| 230 | rh20t_episode_003367 | Insert the pencil into the pencil sharpe | 1 | 0 | 4 | 4 |
| 231 | rh20t_episode_001203 | Wave the flag | 0 | 0 | 4 | 3 |
| 232 | rh20t_episode_002178 | Press the buttons on a row of four power | 0 | 0 | 2 | 4 |
| 233 | rh20t_episode_003146 | Remove the bubble ring from the assemble | 0 | 0 | 4 | 3 |
| 234 | rh20t_episode_000734 | Grab the block and place it at the desig | 1 | 1 | 4 | 4 |
| 235 | rh20t_episode_002349 | Build with small Lego blocks for the nth | 1 | 0 | 4 | 4 |
| 236 | rh20t_episode_000106 | Press the button from top to bottom | 1 | 0 | 2 | 2 |
| 237 | rh20t_episode_000932 | Place the block on the scale | 1 | 1 | 4 | 4 |
| 238 | rh20t_episode_002403 | Build with large Megabloks for the nth t | 1 | 1 | 4 | 4 |
| 239 | rh20t_episode_001649 | Place the brush on the pen rack | 0 | 0 | 4 | 3 |
| 23 | rlbench_episode_000875 | push the maroon button, then push the gr | 0 | 0 | 6 | 3 |
| 240 | rh20t_episode_000666 | Grab the block and place it at the desig | 1 | 1 | 4 | 4 |
| 241 | rh20t_episode_003138 | Remove the bubble ring from the assemble | 0 | 0 | 4 | 3 |
| 242 | rh20t_episode_002471 | Assemble one piece of a puzzle | 1 | 0 | 4 | 4 |
| 243 | rh20t_episode_000122 | Pull out a napkin | 1 | 0 | 3 | 3 |
| 244 | rh20t_episode_003447 | Insert the tip of a large pipette into t | 1 | 1 | 4 | 4 |
| 245 | rh20t_episode_001354 | Cover the box | 0 | 0 | 4 | 3 |
| 246 | rh20t_episode_002923 | Open the microwave door | 1 | 1 | 3 | 3 |
| 247 | rh20t_episode_000412 | Pick up the small block on the left and  | 0 | 1 | 3 | 4 |
| 248 | rh20t_episode_003165 | Move an object from one box to another | 1 | 1 | 4 | 4 |
| 249 | rh20t_episode_001187 | Turn off the desk lamp by pressing the b | 1 | 0 | 2 | 2 |
| 24 | rlbench_episode_001756 | turn right tap | 1 | 1 | 3 | 3 |
| 250 | rh20t_episode_002359 | Build with small Lego blocks for the nth | 1 | 1 | 4 | 4 |
| 251 | rh20t_episode_001670 | Put the cup on the cup rack | 1 | 0 | 4 | 4 |
| 252 | rh20t_episode_000759 | Take out one Hanoi block and throw it as | 1 | 0 | 4 | 4 |
| 253 | rh20t_episode_001619 | Pick up a bag of things | 1 | 0 | 2 | 2 |
| 254 | rh20t_episode_003512 | Insert the tip of a small pipette into t | 1 | 1 | 4 | 4 |
| 255 | rh20t_episode_001012 | Play the drum | 0 | 0 | 4 | 3 |
| 256 | rh20t_episode_002423 | Press a button from top to bottom with o | 0 | 0 | 2 | 3 |
| 257 | rh20t_episode_002464 | Assemble one piece of a puzzle | 0 | 0 | 4 | 3 |
| 258 | rh20t_episode_003542 | Transfer all large pipette tips from one | 1 | 1 | 4 | 4 |
| 259 | rh20t_episode_002289 | Put the toilet paper on its holder | 1 | 0 | 4 | 4 |
| 25 | rlbench_episode_000101 | put the ring on the azure spoke | 1 | 1 | 4 | 4 |
| 260 | rh20t_episode_001502 | Pick up the cup | 0 | 0 | 4 | 3 |
| 261 | rh20t_episode_002892 | Open the microwave door | 1 | 1 | 3 | 3 |
| 262 | rh20t_episode_001014 | Play the drum | 0 | 0 | 4 | 3 |
| 263 | rh20t_episode_002789 | Stack blocks (small Lego) one on top of  | 1 | 0 | 4 | 4 |
| 264 | rh20t_episode_003689 | Chop the orange | 0 | 0 | 4 | 3 |
| 265 | rh20t_episode_003584 | Chop the green garlic | 0 | 0 | 4 | 4 |
| 266 | rh20t_episode_003448 | Insert the tip of a large pipette into t | 1 | 0 | 4 | 4 |
| 267 | rh20t_episode_000888 | Push the soccer ball into the goal | 1 | 0 | 2 | 2 |
| 268 | rh20t_episode_003664 | Chop the onions | 0 | 0 | 4 | 4 |
| 269 | rh20t_episode_001089 | Put the pen into the pen holder | 1 | 1 | 4 | 4 |
| 26 | rlbench_episode_000155 | put the ring on the rose spoke | 1 | 1 | 4 | 4 |
| 270 | rh20t_episode_003719 | Chop the pakchoi | 1 | 0 | 4 | 4 |
| 271 | rh20t_episode_001825 | Rotate the steering wheel 90 degrees cou | 1 | 1 | 3 | 3 |
| 272 | rh20t_episode_003363 | Insert the pencil into the pencil sharpe | 1 | 0 | 4 | 4 |
| 273 | rh20t_episode_003653 | Slice the carrots | 0 | 0 | 3 | 4 |
| 274 | rh20t_episode_001030 | Hit the pool ball | 1 | 0 | 3 | 3 |
| 275 | rh20t_episode_000908 | Push the soccer ball into the goal | 1 | 0 | 2 | 2 |
| 276 | rh20t_episode_002356 | Build with small Lego blocks for the nth | 1 | 1 | 4 | 4 |
| 277 | rh20t_episode_002244 | Turn the knob to decrease the volume of  | 0 | 0 | 3 | 2 |
| 278 | rh20t_episode_003322 | Drag the plate back after holding it dow | 1 | 0 | 3 | 3 |
| 279 | rh20t_episode_000130 | Pull out a napkin | 1 | 0 | 3 | 3 |
| 27 | rlbench_episode_001197 | put the money away in the safe on the bo | 1 | 0 | 4 | 4 |
| 280 | rh20t_episode_000126 | Pull out a napkin | 1 | 1 | 3 | 3 |
| 281 | rh20t_episode_003593 | Chop the green garlic | 0 | 0 | 3 | 4 |
| 282 | rh20t_episode_001270 | Use the gripper to push and close the dr | 1 | 0 | 2 | 2 |
| 283 | rh20t_episode_002149 | Press the buttons on a row of four power | 1 | 0 | 8 | 8 |
| 284 | rh20t_episode_001177 | Turn off the desk lamp by pressing the b | 0 | 0 | 2 | 3 |
| 285 | rh20t_episode_000880 | Push the soccer ball into the goal | 1 | 1 | 2 | 2 |
| 286 | rh20t_episode_003148 | Dial a number on an old rotary phone | 0 | 1 | 3 | 4 |
| 287 | rh20t_episode_002751 | Finish setting up the starting position  | 1 | 0 | 3 | 3 |
| 288 | rh20t_episode_001568 | Screw the lid onto the jar | 0 | 0 | 4 | 4 |
| 289 | rh20t_episode_002036 | Grasp the moving object | 1 | 0 | 2 | 2 |
| 28 | rlbench_episode_000201 | screw in the azure light bulb | 0 | 0 | 4 | 4 |
| 290 | rh20t_episode_003675 | Chop the onions | 0 | 0 | 4 | 4 |
| 291 | rh20t_episode_003286 | Scrub the table with a brush | 0 | 0 | 4 | 4 |
| 292 | rh20t_episode_001590 | Unscrew the lid from the jar | 1 | 0 | 3 | 3 |
| 293 | rh20t_episode_001661 | Place the brush on the pen rack | 1 | 0 | 4 | 4 |
| 294 | rh20t_episode_000364 | Pick up the small block on the left and  | 1 | 1 | 4 | 4 |
| 295 | rh20t_episode_001003 | Play the drum | 0 | 0 | 4 | 3 |
| 296 | rh20t_episode_000465 | Approach and touch the side of the small | 1 | 0 | 2 | 2 |
| 297 | taco_play_episode_001029 | grasp the pink block, then rotate it lef | 1 | 1 | 3 | 3 |
| 298 | taco_play_episode_002129 | go towards the yellow block and pick it  | 1 | 1 | 2 | 2 |
| 299 | taco_play_episode_000897 | go towards the pink block and lift it | 1 | 0 | 3 | 3 |
| 29 | rlbench_episode_000808 | push the maroon button, then push the gr | 0 | 0 | 6 | 3 |
| 300 | taco_play_episode_001532 | turn off the green led light | 0 | 0 | 2 | 3 |
| 301 | taco_play_episode_000933 | put the yellow block on the table | 1 | 1 | 4 | 4 |
| 302 | taco_play_episode_002185 | turn off the green light | 0 | 0 | 2 | 3 |
| 303 | taco_play_episode_002823 | grasp the handle of the drawer, then ope | 0 | 0 | 3 | 2 |
| 304 | taco_play_episode_002762 | take the purple block and rotate it righ | 1 | 0 | 3 | 3 |
| 305 | taco_play_episode_000007 | rotate the pink block towards the right | 1 | 0 | 3 | 3 |
| 306 | taco_play_episode_002172 | push the sliding door to the left | 1 | 0 | 2 | 2 |
| 307 | taco_play_episode_002956 | put the yellow block on the table | 1 | 1 | 4 | 4 |
| 308 | taco_play_episode_001559 | store the grasped pink object in the box | 1 | 1 | 4 | 4 |
| 309 | taco_play_episode_002908 | switch off the blue light | 0 | 0 | 2 | 3 |
| 30 | rlbench_episode_001297 | use the stick to drag the cube onto the  | 0 | 0 | 3 | 4 |
| 310 | taco_play_episode_000389 | put the grasped yellow block inside the  | 1 | 1 | 4 | 4 |
| 311 | taco_play_episode_002990 | stack the yellow block on top of the pur | 1 | 1 | 4 | 4 |
| 312 | taco_play_episode_000556 | put the yellow block on top of the drawe | 1 | 1 | 4 | 4 |
| 313 | taco_play_episode_001761 | go towards the yellow block and lift it | 1 | 0 | 3 | 3 |
| 314 | taco_play_episode_003221 | push the door to the left | 1 | 0 | 2 | 2 |
| 315 | taco_play_episode_000909 | place the grasped yellow block inside th | 1 | 0 | 4 | 4 |
| 316 | taco_play_episode_002166 | pick up the purple block | 1 | 0 | 2 | 2 |
| 317 | taco_play_episode_000816 | put the yellow object on top of the draw | 1 | 1 | 4 | 4 |
| 318 | taco_play_episode_001968 | store the grasped pink object in the box | 1 | 1 | 4 | 4 |
| 319 | taco_play_episode_002875 | place the yellow object on the table | 1 | 0 | 4 | 4 |
| 31 | rlbench_episode_000123 | put the ring on the orange spoke | 1 | 1 | 4 | 4 |
| 320 | taco_play_episode_001508 | grasp the pink block | 1 | 0 | 2 | 2 |
| 321 | taco_play_episode_000397 | move the red light switch to turn on the | 0 | 0 | 2 | 3 |
| 322 | taco_play_episode_001794 | push the sliding door to the left | 1 | 0 | 2 | 2 |
| 323 | taco_play_episode_002099 | put the purple block inside the box | 1 | 1 | 4 | 4 |
| 324 | taco_play_episode_001819 | turn off the red led light | 0 | 0 | 3 | 3 |
| 325 | taco_play_episode_000733 | push the drawer | 1 | 0 | 2 | 2 |
| 326 | taco_play_episode_000781 | put the pink block inside the right cabi | 1 | 1 | 4 | 4 |
| 327 | taco_play_episode_000589 | move to the box, then place the pink obj | 1 | 1 | 4 | 4 |
| 328 | taco_play_episode_000129 | grasp the yellow block, then rotate it r | 1 | 1 | 3 | 3 |
| 329 | taco_play_episode_000696 | place the yellow object on top of the dr | 1 | 1 | 4 | 4 |
| 32 | rlbench_episode_001134 | put the money away in the safe on the mi | 1 | 0 | 4 | 4 |
| 330 | taco_play_episode_002674 | move the blue light switch to turn off t | 0 | 0 | 2 | 3 |
| 331 | taco_play_episode_002109 | take the yellow block and rotate it righ | 1 | 0 | 3 | 3 |
| 332 | taco_play_episode_002968 | slide the door to the left side | 1 | 0 | 3 | 3 |
| 333 | taco_play_episode_000672 | toggle the green light switch to turn on | 0 | 0 | 2 | 3 |
| 334 | taco_play_episode_002768 | place the grasped pink block inside the  | 0 | 0 | 4 | 4 |
| 335 | taco_play_episode_002696 | put the yellow object inside the right c | 1 | 1 | 4 | 4 |
| 336 | taco_play_episode_002147 | put the pink block inside the right cabi | 1 | 1 | 4 | 4 |
| 337 | taco_play_episode_002974 | push the yellow block to the left | 1 | 0 | 2 | 2 |
| 338 | taco_play_episode_001586 | put the pink object inside the left cabi | 0 | 0 | 4 | 4 |
| 339 | taco_play_episode_000717 | push the purple block to the left | 1 | 0 | 2 | 2 |
| 33 | rlbench_episode_000464 | open the top drawer | 0 | 0 | 3 | 4 |
| 340 | taco_play_episode_002480 | place the pink block in the drawer | 1 | 1 | 4 | 4 |
| 341 | taco_play_episode_002478 | place the grasped pink block inside the  | 1 | 1 | 4 | 4 |
| 342 | taco_play_episode_000605 | slide the door to the left, then let it  | 0 | 0 | 4 | 2 |
| 343 | taco_play_episode_000103 | turn off the blue light lamp | 1 | 0 | 3 | 3 |
| 344 | taco_play_episode_000068 | put the pink object inside the right cab | 1 | 1 | 4 | 4 |
| 345 | taco_play_episode_002941 | put the pink block on top of the drawer | 1 | 1 | 4 | 4 |
| 346 | taco_play_episode_000472 | push the door to the left side | 1 | 0 | 2 | 2 |
| 347 | taco_play_episode_002382 | go towards the yellow block and grasp it | 1 | 0 | 2 | 2 |
| 348 | taco_play_episode_000641 | put the grasped purple object inside the | 1 | 1 | 4 | 4 |
| 349 | taco_play_episode_001967 | move the blue light switch to turn on th | 0 | 0 | 2 | 3 |
| 34 | rlbench_episode_000078 | close the azure jar | 0 | 0 | 4 | 3 |
| 350 | taco_play_episode_000889 | place the yellow object on top of the dr | 1 | 1 | 4 | 4 |
| 351 | taco_play_episode_000961 | place the pink block on the table | 1 | 1 | 4 | 4 |
| 352 | taco_play_episode_000131 | grasp the pink block | 1 | 0 | 2 | 2 |
| 353 | taco_play_episode_001143 | put the yellow object on top of the draw | 1 | 1 | 4 | 4 |
| 354 | taco_play_episode_000968 | put the grasped yellow object inside the | 1 | 1 | 4 | 4 |
| 355 | taco_play_episode_001330 | go slide the purple block to the left | 0 | 0 | 3 | 2 |
| 356 | taco_play_episode_002266 | place the yellow object inside the box | 1 | 1 | 4 | 4 |
| 357 | taco_play_episode_001093 | grasp the door handle, then move the doo | 1 | 1 | 3 | 3 |
| 358 | taco_play_episode_002654 | turn off the red led light | 0 | 0 | 2 | 3 |
| 359 | taco_play_episode_001481 | place the purple object on top of the dr | 1 | 1 | 4 | 4 |
| 35 | rlbench_episode_000185 | put the ring on the purple spoke | 1 | 1 | 4 | 4 |
| 360 | taco_play_episode_001178 | store the grasped yellow object in the d | 1 | 0 | 4 | 4 |
| 361 | taco_play_episode_002459 | grasp the drawer handle and close it | 1 | 0 | 3 | 3 |
| 362 | taco_play_episode_001900 | go push the yellow block to the right | 0 | 0 | 2 | 3 |
| 363 | taco_play_episode_000280 | grasp the drawer handle, then open it | 0 | 0 | 3 | 2 |
| 364 | taco_play_episode_001600 | open the cabinet drawer | 1 | 1 | 3 | 3 |
| 365 | taco_play_episode_002077 | push the red button to turn off the red  | 1 | 0 | 2 | 2 |
| 366 | jaco_play_episode_000747 | pick up the milk dairy | 1 | 1 | 4 | 4 |
| 367 | jaco_play_episode_000660 | pick up the square bread | 0 | 0 | 2 | 3 |
| 368 | jaco_play_episode_000915 | pick up the burger meat | 1 | 0 | 2 | 2 |
| 369 | jaco_play_episode_000587 | place the milk dairy in the blue bowl | 1 | 1 | 4 | 4 |
| 36 | rlbench_episode_000967 | put the crackers in the cupboard | 1 | 0 | 4 | 4 |
| 370 | jaco_play_episode_000477 | place the orange fruit in the sink | 1 | 1 | 4 | 4 |
| 371 | jaco_play_episode_000928 | place the yellow cup in the oven | 1 | 1 | 4 | 4 |
| 372 | jaco_play_episode_000568 | place the gray bowl in the dish rack | 1 | 1 | 4 | 4 |
| 373 | jaco_play_episode_000144 | place the long bread in the table | 1 | 1 | 4 | 4 |
| 374 | jaco_play_episode_000603 | pick up the burger meat | 1 | 0 | 2 | 2 |
| 375 | jaco_play_episode_000169 | place the gray bowl in the oven | 1 | 0 | 4 | 4 |
| 376 | jaco_play_episode_000595 | pick up the green cup | 0 | 0 | 2 | 3 |
| 377 | jaco_play_episode_000578 | pick up the orange fruit | 0 | 0 | 2 | 3 |
| 378 | jaco_play_episode_000021 | place the green cup in the gray plate | 1 | 1 | 4 | 4 |
| 379 | jaco_play_episode_000499 | pick up the apple fruit | 0 | 0 | 2 | 3 |
| 37 | rlbench_episode_000928 | put the soup in the cupboard | 1 | 0 | 4 | 4 |
| 380 | jaco_play_episode_000875 | place the gray bowl in the sink | 1 | 1 | 4 | 4 |
| 381 | jaco_play_episode_000206 | pick up the square bread | 0 | 0 | 2 | 3 |
| 382 | jaco_play_episode_000689 | place the milk dairy in the white plate | 1 | 1 | 4 | 4 |
| 383 | jaco_play_episode_000004 | pick up the orange fruit | 0 | 0 | 2 | 3 |
| 384 | jaco_play_episode_000874 | pick up the long bread | 0 | 0 | 4 | 2 |
| 385 | jaco_play_episode_000899 | pick up the gray bowl | 0 | 0 | 2 | 3 |
| 386 | jaco_play_episode_000166 | place the burger meat in the sink | 1 | 1 | 4 | 4 |
| 387 | jaco_play_episode_000194 | place the orange fruit in the gray plate | 1 | 1 | 4 | 4 |
| 388 | jaco_play_episode_000156 | pick up the apple fruit | 0 | 0 | 4 | 2 |
| 389 | jaco_play_episode_000536 | pick up the milk dairy | 0 | 0 | 4 | 2 |
| 38 | rlbench_episode_000150 | put the ring on the olive spoke | 1 | 1 | 4 | 4 |
| 390 | jaco_play_episode_000701 | place the square bread in the sink | 1 | 1 | 4 | 4 |
| 391 | jaco_play_episode_000817 | place the square bread in the blue bowl | 1 | 1 | 4 | 4 |
| 392 | jaco_play_episode_000134 | place the steak meat in the oven | 1 | 1 | 4 | 4 |
| 393 | jaco_play_episode_000630 | pick up the black bowl | 1 | 0 | 2 | 2 |
| 394 | jaco_play_episode_000069 | place the black bowl in the oven | 1 | 0 | 4 | 4 |
| 395 | jaco_play_episode_000369 | place the milk dairy in the table | 1 | 1 | 4 | 4 |
| 396 | jaco_play_episode_000768 | place the square bread in the blue bowl | 1 | 1 | 4 | 4 |
| 397 | jaco_play_episode_000588 | place the butter dairy in the sink | 1 | 1 | 4 | 4 |
| 398 | jaco_play_episode_000602 | pick up the orange fruit | 0 | 0 | 4 | 3 |
| 399 | jaco_play_episode_000629 | pick up the steak meat | 1 | 0 | 2 | 2 |
| 39 | rlbench_episode_000525 | place 3 cups on the cup holder | 0 | 0 | 12 | 6 |
| 400 | jaco_play_episode_000548 | pick up the yellow cup | 0 | 0 | 4 | 3 |
| 401 | jaco_play_episode_000883 | pick up the orange fruit | 0 | 0 | 4 | 3 |
| 402 | jaco_play_episode_000117 | pick up the orange fruit | 1 | 0 | 2 | 2 |
| 403 | jaco_play_episode_000634 | pick up the orange fruit | 0 | 0 | 2 | 3 |
| 404 | jaco_play_episode_000064 | pick up the black bowl | 1 | 0 | 2 | 2 |
| 405 | jaco_play_episode_000279 | place the gray bowl in the oven | 1 | 0 | 4 | 4 |
| 406 | jaco_play_episode_000215 | place the milk dairy in the sink | 1 | 1 | 4 | 4 |
| 407 | jaco_play_episode_000314 | place the orange fruit in the gray plate | 1 | 1 | 4 | 4 |
| 408 | jaco_play_episode_000049 | place the green cup in the dish rack | 1 | 1 | 4 | 4 |
| 409 | jaco_play_episode_000869 | place the orange fruit in the table | 1 | 0 | 4 | 4 |
| 40 | rlbench_episode_000194 | put the ring on the violet spoke | 1 | 1 | 4 | 4 |
| 410 | jaco_play_episode_000109 | place the butter dairy in the sink | 1 | 1 | 4 | 4 |
| 411 | jaco_play_episode_000574 | place the burger meat in the oven | 1 | 0 | 4 | 4 |
| 412 | jaco_play_episode_000513 | place the milk dairy in the sink | 1 | 1 | 4 | 4 |
| 413 | jaco_play_episode_000636 | pick up the square bread | 0 | 0 | 4 | 3 |
| 414 | jaco_play_episode_000032 | place the black bowl in the gray plate | 1 | 1 | 4 | 4 |
| 415 | jaco_play_episode_000857 | pick up the butter dairy | 0 | 1 | 4 | 3 |
| 416 | jaco_play_episode_000070 | pick up the steak meat | 0 | 0 | 4 | 2 |
| 417 | jaco_play_episode_000502 | place the green cup in the oven | 1 | 0 | 4 | 4 |
| 418 | jaco_play_episode_000695 | place the gray bowl in the gray plate | 1 | 1 | 4 | 4 |
| 419 | jaco_play_episode_000572 | place the long bread in the table | 1 | 1 | 4 | 4 |
| 41 | rlbench_episode_001229 | use the stick to drag the cube onto the  | 0 | 0 | 3 | 4 |
| 420 | jaco_play_episode_000686 | pick up the milk dairy | 0 | 0 | 4 | 2 |
| 421 | jaco_play_episode_000580 | place the apple fruit in the gray plate | 1 | 1 | 4 | 4 |
| 422 | jaco_play_episode_000224 | place the gray bowl in the oven | 1 | 1 | 4 | 4 |
| 423 | jaco_play_episode_000782 | pick up the milk dairy | 0 | 0 | 2 | 3 |
| 424 | jaco_play_episode_000575 | pick up the gray bowl | 0 | 1 | 4 | 3 |
| 425 | jaco_play_episode_000605 | pick up the black bowl | 1 | 0 | 2 | 2 |
| 426 | jaco_play_episode_000907 | place the milk dairy in the gray bowl | 1 | 1 | 4 | 4 |
| 427 | jaco_play_episode_000543 | place the yellow cup in the table | 1 | 1 | 4 | 4 |
| 428 | jaco_play_episode_000278 | pick up the gray bowl | 0 | 0 | 2 | 3 |
| 429 | jaco_play_episode_000788 | place the butter dairy in the black bowl | 1 | 1 | 4 | 4 |
| 42 | rlbench_episode_000944 | put the chocolate jello in the cupboard | 1 | 0 | 4 | 4 |
| 430 | jaco_play_episode_000594 | pick up the green cup | 0 | 0 | 2 | 3 |
| 431 | jaco_play_episode_000293 | pick up the gray bowl | 1 | 0 | 2 | 2 |
| 432 | jaco_play_episode_000633 | pick up the milk dairy | 1 | 0 | 2 | 2 |
| 433 | jaco_play_episode_000227 | pick up the orange fruit | 0 | 0 | 2 | 3 |
| 434 | jaco_play_episode_000942 | place the black bowl in the dish rack | 1 | 1 | 4 | 4 |
| 435 | fractal20220817_data_episode_059918 | move redbull can near sponge | 1 | 1 | 4 | 4 |
| 436 | fractal20220817_data_episode_019362 | move paper bowl near green can | 1 | 1 | 4 | 4 |
| 437 | fractal20220817_data_episode_055887 | place coke can into white bowl | 1 | 0 | 4 | 4 |
| 438 | fractal20220817_data_episode_016864 | place redbull can upright | 1 | 1 | 4 | 4 |
| 439 | fractal20220817_data_episode_052390 | move coke can near green rice chip bag | 1 | 0 | 4 | 4 |
| 43 | rlbench_episode_000126 | put the ring on the teal spoke | 1 | 1 | 4 | 4 |
| 440 | fractal20220817_data_episode_058888 | place brown chip bag into bottom drawer | 1 | 0 | 4 | 4 |
| 441 | fractal20220817_data_episode_042147 | move blue plastic bottle near green jala | 1 | 1 | 4 | 4 |
| 442 | fractal20220817_data_episode_010565 | pick blue plastic bottle | 0 | 1 | 2 | 3 |
| 443 | fractal20220817_data_episode_086891 | move brown chip bag near sponge | 0 | 0 | 4 | 4 |
| 444 | fractal20220817_data_episode_033365 | pick green jalapeno chip bag from top dr | 1 | 1 | 4 | 4 |
| 445 | fractal20220817_data_episode_057267 | place water bottle into bottom drawer | 1 | 1 | 4 | 4 |
| 446 | fractal20220817_data_episode_010582 | pick brown chip bag from middle drawer a | 1 | 1 | 4 | 4 |
| 447 | fractal20220817_data_episode_029700 | place orange can into bottom drawer | 1 | 1 | 4 | 4 |
| 448 | fractal20220817_data_episode_086787 | pick sponge from middle drawer and place | 1 | 1 | 4 | 4 |
| 449 | fractal20220817_data_episode_040576 | knock blue plastic bottle over | 0 | 0 | 2 | 3 |
| 44 | rlbench_episode_001260 | use the stick to drag the cube onto the  | 0 | 0 | 3 | 4 |
| 450 | fractal20220817_data_episode_016894 | move green can near blue plastic bottle | 1 | 0 | 4 | 4 |
| 451 | fractal20220817_data_episode_021732 | place blue plastic bottle upright | 1 | 1 | 4 | 4 |
| 452 | fractal20220817_data_episode_083721 | pick rxbar chocolate from middle drawer  | 1 | 1 | 4 | 4 |
| 453 | fractal20220817_data_episode_085730 | pick coke can from bottom drawer and pla | 1 | 1 | 4 | 4 |
| 454 | fractal20220817_data_episode_048815 | pick blue plastic bottle from top drawer | 1 | 1 | 4 | 4 |
| 455 | fractal20220817_data_episode_020101 | knock pepsi can over | 0 | 0 | 2 | 3 |
| 456 | fractal20220817_data_episode_034641 | knock water bottle over | 0 | 0 | 2 | 3 |
| 457 | fractal20220817_data_episode_019394 | place green can into middle drawer | 0 | 0 | 4 | 4 |
| 458 | fractal20220817_data_episode_062578 | pick green rice chip bag | 0 | 0 | 2 | 3 |
| 459 | fractal20220817_data_episode_030557 | office manipulation | 1 | 0 | 4 | 4 |
| 45 | rlbench_episode_000263 | screw in the blue light bulb | 0 | 0 | 4 | 4 |
| 460 | fractal20220817_data_episode_013067 | pick redbull can from middle drawer and  | 1 | 1 | 4 | 4 |
| 461 | fractal20220817_data_episode_053194 | pick coke can | 1 | 0 | 2 | 2 |
| 462 | fractal20220817_data_episode_064841 | pick sponge from white bowl and place on | 1 | 0 | 4 | 4 |
| 463 | fractal20220817_data_episode_022786 | place brown chip bag into white bowl | 1 | 1 | 4 | 4 |
| 464 | fractal20220817_data_episode_086688 | place green can upright | 1 | 0 | 4 | 4 |
| 465 | fractal20220817_data_episode_031152 | move green rice chip bag near redbull ca | 1 | 1 | 4 | 4 |
| 466 | fractal20220817_data_episode_022627 | pick green jalapeno chip bag from bottom | 1 | 1 | 4 | 4 |
| 467 | fractal20220817_data_episode_057569 | move green can near blue chip bag | 1 | 0 | 4 | 4 |
| 468 | fractal20220817_data_episode_068382 | pick green rice chip bag from top drawer | 1 | 1 | 4 | 4 |
| 469 | fractal20220817_data_episode_054312 | move green rice chip bag near rxbar choc | 0 | 0 | 4 | 4 |
| 46 | rlbench_episode_000486 | open the middle drawer | 1 | 1 | 3 | 3 |
| 470 | fractal20220817_data_episode_045208 | pick orange from white bowl | 1 | 0 | 3 | 3 |
| 471 | fractal20220817_data_episode_056409 | open top drawer | 0 | 1 | 2 | 3 |
| 472 | fractal20220817_data_episode_027416 | place green can into bottom drawer | 1 | 1 | 4 | 4 |
| 473 | fractal20220817_data_episode_047234 | place rxbar blueberry into bottom drawer | 1 | 1 | 4 | 4 |
| 474 | fractal20220817_data_episode_042571 | pick apple from white bowl | 0 | 0 | 4 | 3 |
| 475 | fractal20220817_data_episode_012899 | pick rxbar blueberry from top drawer and | 1 | 1 | 4 | 4 |
| 476 | fractal20220817_data_episode_048789 | pick green can from bottom drawer and pl | 1 | 1 | 4 | 4 |
| 477 | fractal20220817_data_episode_003624 | pick rxbar chocolate from middle drawer  | 1 | 1 | 4 | 4 |
| 478 | fractal20220817_data_episode_045103 | pick pepsi can from bottom shelf of frid | 0 | 0 | 4 | 3 |
| 479 | fractal20220817_data_episode_072429 | pick 7up can | 1 | 0 | 2 | 2 |
| 47 | rlbench_episode_001705 | turn left tap | 0 | 0 | 3 | 4 |
| 480 | fractal20220817_data_episode_061457 | pick sponge | 0 | 0 | 2 | 3 |
| 481 | fractal20220817_data_episode_058557 | place redbull can upright | 0 | 1 | 4 | 4 |
| 482 | fractal20220817_data_episode_003459 | move green rice chip bag near water bott | 1 | 0 | 4 | 4 |
| 483 | fractal20220817_data_episode_051076 | move redbull can near blue chip bag | 0 | 0 | 4 | 4 |
| 484 | fractal20220817_data_episode_044067 | pick banana from white bowl | 1 | 0 | 3 | 3 |
| 485 | fractal20220817_data_episode_068579 | place apple into middle drawer | 1 | 1 | 4 | 4 |
| 486 | fractal20220817_data_episode_081476 | move rxbar chocolate near sponge | 1 | 1 | 4 | 4 |
| 487 | fractal20220817_data_episode_039630 | place orange into middle drawer | 1 | 1 | 4 | 4 |
| 488 | fractal20220817_data_episode_067950 | pick coke can from middle drawer and pla | 1 | 1 | 4 | 4 |
| 489 | fractal20220817_data_episode_009401 | knock green can over | 0 | 0 | 2 | 3 |
| 48 | rlbench_episode_001698 | sweep dirt to the short dustpan | 1 | 0 | 4 | 4 |
| 490 | fractal20220817_data_episode_015885 | pick green rice chip bag | 0 | 0 | 2 | 3 |
| 491 | fractal20220817_data_episode_031831 | place blue chip bag into white bowl | 1 | 1 | 4 | 4 |
| 492 | fractal20220817_data_episode_014599 | knock coke can over | 0 | 0 | 2 | 3 |
| 493 | fractal20220817_data_episode_011989 | place green can into bottom drawer | 1 | 1 | 4 | 4 |
| 494 | fractal20220817_data_episode_036484 | pick green jalapeno chip bag | 0 | 0 | 2 | 3 |
| 495 | fractal20220817_data_episode_037399 | move water bottle near sponge | 1 | 1 | 4 | 4 |
| 496 | fractal20220817_data_episode_006214 | knock green can over | 0 | 0 | 2 | 3 |
| 497 | fractal20220817_data_episode_025596 | open top drawer | 1 | 0 | 2 | 2 |
| 498 | fractal20220817_data_episode_037103 | move sponge near rxbar blueberry | 1 | 0 | 4 | 4 |
| 499 | fractal20220817_data_episode_017969 | place sponge into middle drawer | 1 | 1 | 4 | 4 |
| 49 | rlbench_episode_000132 | put the ring on the green spoke | 1 | 1 | 4 | 4 |
| 500 | fractal20220817_data_episode_056521 | open bottom drawer | 0 | 0 | 2 | 3 |
| 50 | rlbench_episode_001284 | use the stick to drag the cube onto the  | 0 | 0 | 3 | 4 |
| 51 | rlbench_episode_001603 | sweep dirt to the short dustpan | 1 | 0 | 4 | 4 |
| 52 | rlbench_episode_000880 | push the maroon button | 0 | 0 | 2 | 3 |
| 53 | rlbench_episode_000105 | put the ring on the navy spoke | 1 | 1 | 4 | 4 |
| 54 | rlbench_episode_000480 | open the middle drawer | 1 | 1 | 3 | 3 |
| 55 | rlbench_episode_000098 | close the black jar | 1 | 1 | 4 | 4 |
| 56 | rlbench_episode_001241 | use the stick to drag the cube onto the  | 0 | 0 | 3 | 4 |
| 57 | rlbench_episode_000282 | screw in the yellow light bulb | 1 | 0 | 4 | 4 |
| 58 | rlbench_episode_000635 | put the triangular prism in the shape so | 1 | 1 | 4 | 4 |
| 59 | rlbench_episode_000930 | put the crackers in the cupboard | 1 | 1 | 4 | 4 |
| 60 | rlbench_episode_000307 | take the chicken off the grill | 0 | 0 | 4 | 4 |
| 61 | rlbench_episode_001208 | use the stick to drag the cube onto the  | 0 | 0 | 4 | 4 |
| 62 | rlbench_episode_000251 | screw in the white light bulb | 0 | 0 | 4 | 4 |
| 63 | rlbench_episode_001271 | use the stick to drag the cube onto the  | 0 | 0 | 3 | 4 |
| 64 | rlbench_episode_000677 | put the cylinder in the shape sorter | 1 | 1 | 4 | 4 |
| 65 | rlbench_episode_001248 | use the stick to drag the cube onto the  | 0 | 0 | 3 | 4 |
| 66 | rlbench_episode_000389 | take the chicken off the grill | 0 | 0 | 4 | 4 |
| 67 | rlbench_episode_000220 | screw in the green light bulb | 0 | 0 | 4 | 4 |
| 68 | rlbench_episode_001295 | use the stick to drag the cube onto the  | 0 | 0 | 4 | 4 |
| 69 | rlbench_episode_001724 | turn left tap | 0 | 0 | 3 | 4 |
| 70 | rlbench_episode_000405 | open the top drawer | 1 | 1 | 3 | 3 |
| 71 | rlbench_episode_000823 | push the maroon button, then push the gr | 1 | 1 | 4 | 4 |
| 72 | rlbench_episode_000208 | screw in the navy light bulb | 0 | 0 | 4 | 4 |
| 73 | rlbench_episode_001222 | use the stick to drag the cube onto the  | 0 | 0 | 3 | 4 |
| 74 | rlbench_episode_000134 | put the ring on the blue spoke | 1 | 1 | 4 | 4 |
| 75 | rlbench_episode_001257 | use the stick to drag the cube onto the  | 0 | 0 | 3 | 4 |
| 76 | rlbench_episode_000127 | put the ring on the rose spoke | 1 | 1 | 4 | 4 |
| 77 | rlbench_episode_001678 | sweep dirt to the tall dustpan | 1 | 0 | 4 | 4 |
| 78 | rlbench_episode_000442 | open the middle drawer | 1 | 1 | 3 | 3 |
| 79 | rlbench_episode_001109 | put the money away in the safe on the mi | 1 | 0 | 4 | 4 |
| 80 | rlbench_episode_001188 | put the money away in the safe on the mi | 1 | 0 | 4 | 4 |
| 81 | rlbench_episode_000952 | put the mustard in the cupboard | 1 | 0 | 4 | 4 |
| 82 | rlbench_episode_000691 | put the cube in the shape sorter | 1 | 1 | 4 | 4 |
| 83 | rlbench_episode_001035 | put the item in the middle drawer | 1 | 0 | 4 | 4 |
| 84 | rlbench_episode_001008 | put the item in the bottom drawer | 1 | 0 | 4 | 4 |
| 85 | rlbench_episode_000800 | push the maroon button, then push the gr | 0 | 0 | 6 | 3 |
| 86 | rlbench_episode_000656 | put the moon in the shape sorter | 1 | 1 | 4 | 4 |
| 87 | rlbench_episode_000543 | place 3 cups on the cup holder | 0 | 0 | 9 | 6 |
| 88 | rlbench_episode_000387 | take the chicken off the grill | 0 | 0 | 4 | 4 |
| 89 | rlbench_episode_000532 | place 3 cups on the cup holder | 0 | 0 | 9 | 6 |
| 90 | droid_episode_009148 | Pick up the salt cellar and put it in th | 1 | 1 | 4 | 4 |
| 91 | droid_episode_033219 | Remove the green object from the cup | 1 | 1 | 4 | 4 |
| 92 | droid_episode_085535 | Move a letter piece on the table | 0 | 0 | 4 | 3 |
| 93 | droid_episode_076846 | Put the multi USB charging cable in the  | 1 | 1 | 4 | 4 |
| 94 | droid_episode_037884 | Reposition the top remote on the bottom  | 1 | 0 | 4 | 4 |
| 95 | droid_episode_063584 | Pick the orange and yellow blocks and pu | 1 | 0 | 6 | 6 |
| 96 | droid_episode_031717 | Put the wooden spoon with holes on the c | 1 | 1 | 4 | 4 |
| 97 | droid_episode_008169 | Move the black spectacle case to the lef | 1 | 1 | 4 | 4 |
| 98 | droid_episode_013007 | Pick up the pot from the stove and put i | 1 | 1 | 4 | 4 |
| 99 | droid_episode_081716 | Close the cube-shaped object | 1 | 0 | 3 | 3 |

## Per-dataset breakdown
LoRA vs Refined / Base vs Refined, grouped by source dataset.
| Dataset | n | LoRA EM | Base EM | LoRA UV MAE | Base UV MAE | LoRA step-diff | Base step-diff | LoRA hint-tok | Base hint-tok |
|---|---|---|---|---|---|---|---|---|---|
| bridge | 72 | 0.903 | 0.806 | 0.124 | 0.110 | 0.153 | 0.264 | 6.546 | 4.833 |
| droid | 72 | 0.750 | 0.597 | 0.155 | 0.213 | 0.292 | 0.736 | 5.979 | 4.583 |
| fractal20220817_data | 68 | 0.706 | 0.529 | 0.100 | 0.107 | 0.221 | 0.412 | 6.556 | 7.250 |
| jaco_play | 72 | 0.653 | 0.472 | 0.126 | 0.149 | 0.431 | 0.917 | 5.958 | 5.750 |
| rh20t | 72 | 0.625 | 0.278 | 0.156 | 0.122 | 0.306 | 1.042 | 5.738 | 4.983 |
| rlbench | 72 | 0.569 | 0.347 | 0.239 | 0.164 | 0.486 | 0.861 | 6.145 | 5.238 |
| taco_play | 72 | 0.764 | 0.417 | 0.250 | 0.249 | 0.208 | 0.667 | 4.828 | 4.333 |

*Reading this table*: a dataset where LoRA EM ≫ Base EM is one where LoRA learned the training distribution well. A dataset where LoRA step-diff is large (e.g. taco_play) is one where LoRA over-predicts step count — likely a dataset-specific training-label bias rather than a model weakness.


## What to read in this table
- **Action seq EM**: did the pred reproduce the exact ordered action list? High LoRA EM + low Base EM → LoRA learned the training distribution.
- **Affordance UV MAE**: 0 means pred matches label exactly; ~0.25 means roughly random in the unit square. **If `[0.5,0.5] center rate` is high, LoRA collapsed to predicting the image center — i.e., the pointing head did NOT learn.**
- **Hint specificity**: refined label hints have ~5–8 tokens; raw GPT and untrained model produce ~2–3 tokens ('the X'). LoRA close to refined → it learned to copy hints; far → underfit on hint refinement.
- **Has release rate**: training labels often omit release. If LoRA matches that omission rate, it inherited the GPT label bias.