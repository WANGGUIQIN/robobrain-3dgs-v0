# GaussianBrain — ICLR Submission Draft (Abstract + Introduction)

> Draft v0.2 (2026-05-29).  Plan-quality numbers in §1.4 are real (500-episode
> A/B/C probe).  The cross-embodiment closed-loop study is the evaluation
> protocol now in progress (LIBERO + RoboTwin); those cells are marked
> "forthcoming" and contain no invented numbers.  Companion documents:
> `PAPER_PLAN.md` and
> `docs/superpowers/specs/2026-05-29-cross-embodiment-rekep-validation-design.md`.

---

## Title (candidate)

**GaussianBrain: Render-Supervised 3D Gaussian Tokens for Verifiable Embodied Planning in Vision-Language Models**

## Abstract

Vision-language models (VLMs) trained on internet image-text pairs lack the
geometric grounding needed for embodied manipulation: a model that scores well
on visual question answering can still misplace a grasp by tens of
centimeters, and its competence collapses as soon as the camera viewpoint
shifts.  We argue that the bottleneck is *representational*, not data: a
flat 2D token stream cannot encode the metric scene structure that
manipulation reasoning requires.

We propose **GaussianBrain**, a plug-in 3D representation that injects a small
set of 3D Gaussian tokens into a pretrained 8B VLM (Qwen3-VL / RoboBrain 2.5)
alongside its native visual tokens.  Three design choices make the integration
work without retraining the backbone:
(i) **RGBD-deterministic factorization** — Gaussian centers are obtained by
analytic depth back-projection, so the network only learns scale, rotation,
spherical-harmonic appearance, opacity and a per-Gaussian uncertainty;
(ii) **differentiable-rendering supervision** — an auxiliary photometric
+ depth + opacity loss routes geometry-aware gradients back into the VLM,
turning rendering quality into a representation regularizer;
(iii) **uncertainty-aware token budgeting** — farthest-point sampling is
re-weighted by the predicted variance so that the 64-token budget given to
the LLM concentrates on confident geometry.

To make the model's outputs *verifiable*, we further train the LLM on a
structured plan target: each manipulation step emits a part-aware affordance
hint, normalized pixel coordinates, and a typed list of geometric constraints
drawn from a five-category × three-role taxonomy (contact, spatial, pose,
direction, safety × completion, safety, progress).  This converts free-form
plan strings into machine-checkable predicates that a downstream executor or
runtime monitor can verify against the same 3D Gaussian field that produced
them.

Whereas a parallel line of work closes the embodiment-and-viewpoint gap with
*data* — e.g. PhysBrain translates large-scale human egocentric video into
structured supervision for an 8B embodied brain — GaussianBrain closes it with
a *representation*: an explicit, render-supervised 3D geometry that is
camera-invariant by construction.  We curate a 27 K-episode benchmark unifying
twelve robotics datasets (RLBench, DROID, Bridge V2, taco_play, ALOHA, rh20t,
and seven Open X-Embodiment subsets) and evaluate on two complementary axes.
*Offline*, a three-level protocol (seen / unseen / cross-camera) probes the 3D
branch's view-invariance, and a 500-episode A/B/C probe shows that our trained
planner produces markedly better-structured, better-grounded plans than the
un-tuned 8B backbone — most strikingly a +35-point gain in scene-object
grounding (Jaccard 0.66 vs 0.31) and +22 points in action-sequence exact match
(0.71 vs 0.49).  *Closed-loop*, we feed the typed plans to a training-free
relational-keypoint-constraint optimizer and execute them in two simulators of
different embodiment — single-arm LIBERO and dual-arm RoboTwin — isolating the
perception-transfer cost with a privileged-keypoint upper bound.  We release
the data pipeline, training code, and checkpoints.

---

## 1. Introduction

### 1.1 Motivation

Robotic manipulation requires a model to ground a natural-language goal in
the metric geometry of a physical scene: where exactly to grasp, in what
direction to approach, under what contact and pose constraints.  Recent
vision-language-action models — OpenVLA, RT-2, π₀, RoboBrain — have made
striking progress on language conditioning, but their visual stack is still
fundamentally **two-dimensional**: a frozen ViT encodes pixels, the language
model decodes actions or affordances, and any notion of 3D structure must be
re-learned from monocular cues at the cost of view invariance and metric
accuracy.

The cost of this 2D bias surfaces in two failure modes.  First, *spatial
imprecision*: even when an 8B VLM names the correct object, the (u, v)
coordinate it emits is biased toward visual centroids and is unreliable for
contact-rich grasps such as handles, rims and lids.  Second, *view
brittleness*: a model trained from a front camera loses substantial accuracy
when evaluated from a shoulder or wrist view of the same scene, because the
2D feature manifold does not separate geometry from appearance.  Both failure
modes are aggravated by the fact that VLM pretraining cannot include
calibrated RGB-D observations at scale, so any 3D inductive bias must be
introduced at fine-tuning time.

### 1.2 Why existing 3D-VLM approaches are not enough

A growing family of works injects 3D information into language models: 3D-LLM
and LEO consume point clouds, ManipLLM and ShapeLLM operate on object-level
3D primitives, and recent papers (LangSplat, Gaussian Grouping, LERF) attach
language fields to 3D-Gaussian-Splatting reconstructions.  Three limitations
prevent these designs from being used as a drop-in upgrade to a manipulation
VLM:

1. **Optimization-heavy 3D representations.** 3DGS-based scene fields
   typically require per-scene optimization or large feed-forward
   reconstructors; both are at odds with the single-frame, real-time regime
   of a manipulation policy.
2. **Lack of cross-modal supervision back into the VLM.**  Existing systems
   either keep the 3D branch frozen or treat it as a pre-encoded input; few
   provide a gradient signal that *teaches the VLM* to use the 3D modality.
3. **Unstructured outputs.**  Affordance predictions are usually pixel points
   or free-form plans, neither of which a downstream executor can verify.
   When the model is wrong, there is no way to detect it short of running
   the action.

A second, orthogonal response to the same view-and-embodiment gap scales
*data* rather than representation: PhysBrain [arXiv:2512.16793] translates
large-scale human egocentric video into three million structured
vision-question-answer instances and reports closed-loop manipulation success
competitive with RoboBrain 2.5 (67.4 % vs 67.6 %) without collecting new robot
data.  This is complementary to our aim — better data and a better geometric
representation can compose — but it leaves the *representational* bottleneck
untouched: the visual stack stays 2D and plan outputs stay free-form rather
than verifiable.  GaussianBrain instead asks what a geometry-explicit token
stream and a typed, checkable plan can buy, and tests that question in closed
loop *across embodiments*, not only on offline VQA.

### 1.3 Our approach

GaussianBrain attacks all three limitations by making the 3D branch
*lightweight, jointly supervised, and structurally-output-typed*.

**A deterministic-Gaussian feed-forward 3D head.**  Given one RGB-D frame and
intrinsics, we back-project depth to obtain Gaussian centers analytically
and train a small CNN to predict the remaining parameters (scale,
quaternion rotation, spherical-harmonic colour, opacity, and a per-Gaussian
variance).  This reduces 3D representation learning to per-pixel regression
and runs at a few milliseconds per frame.

**A PointNet++ tokenizer with uncertainty-aware FPS.**  A three-level
hierarchical aggregator compresses 2 048 Gaussians into 64 tokens; the
farthest-point-sampling step is biased so that high-variance Gaussians are
sampled less often, concentrating the LLM's budget on confident geometry.
Tokens are projected to the LLM's hidden dimension, tagged with a learnable
type embedding, and prepended to the standard image+text sequence.

**Differentiable rendering as a representation regularizer.**  We train the
3D branch jointly with the LLM under a combined objective
`L = L_lm + 0.3 · L_render`, where `L_render` is a photometric + depth +
opacity + variance loss evaluated on a tile-free differentiable rasterizer.
This is the key mechanism by which geometric supervision flows back through
the GS tokens into the LLM's gradient path, encouraging the language head to
make use of geometrically meaningful features rather than overfit to 2D
patterns.

**A typed plan output for verification.**  The LLM is supervised to emit
each manipulation step as a quadruple of *(action, target, part-aware
affordance hint, structured constraints)* with constraints drawn from a
five-category × three-role taxonomy.  Because every predicate is grounded in
either 3D distances or pose primitives, downstream verifiers — including a
LangSAM-based test-time refinement we report as an ablation — can be wired
directly to the same Gaussian field the model emitted.

### 1.4 Empirical results

We train a parameter-efficient LoRA planner (rank-16 on q/k/v/o); on this
planning objective LoRA matches or exceeds a partial full fine-tune at a
fraction of the trainable parameters, so we adopt it throughout.

**Offline plan quality (done, n = 500).**  An A/B/C probe scores three plan
sources against a refined ground-truth label, per episode, across seven
dataset families: (A) the un-tuned 8B backbone, (B) the raw upstream label,
and (C) our LoRA planner.  Our planner improves plan *structure* decisively
over the backbone — action-sequence exact match 0.71 vs 0.49 (+22 pts),
action-set Jaccard 0.89 vs 0.77, per-step target grounding 0.78 vs 0.55
(+23 pts), and, the largest gap, scene-object grounding 0.66 vs 0.31
(+35 pts).  Affordance UV error is statistically tied (0.165 vs 0.162): the
keypoint location is bottlenecked by the LangSAM grounder, not the planner,
which is precisely why the closed-loop study below uses a direct-UV keypoint
path.  The mode-collapse failure of the pre-fix model — all affordances at the
image center — is fully eliminated (center rate 0.000), and grounding succeeds
on 99.1 % of steps.

**Representation ablations (three-level protocol, in progress).**  On the
seen / unseen / cross-camera protocol we isolate the 3D branch: removing the
rendering loss is expected to collapse cross-camera affordance accuracy toward
the 2D-only baseline, a raw point cloud at matched token budget to forfeit a
large fraction of the gain, and uncertainty-weighted FPS to add a margin that
grows with scene complexity.  These cross-camera sweeps are running.

**Closed-loop cross-embodiment (protocol; results forthcoming).**  To test the
typed plans in *execution* — the regime in which data-centric embodied brains
such as PhysBrain are measured — we feed each plan's keypoints and typed
constraints to a training-free relational-keypoint-constraint (ReKep-style)
optimizer that solves for SE(3) sub-goals, and execute them in two simulators
of different embodiment: single-arm LIBERO (robosuite/MuJoCo) and dual-arm
RoboTwin (SAPIEN).  We report task success under each benchmark's native
checker for two keypoint sources that share the entire downstream stack — a
*privileged* upper bound from ground-truth object poses, and the *frozen-VLM*
keypoints — so their gap measures exactly the planner's perception-transfer
cost to an unseen embodiment.  A test-time LangSAM refinement, conditioned on
the model's part-aware hint rather than the bare object name, is reported as an
ablation.

### 1.5 Contributions

* **A render-supervised 3D Gaussian token branch** that plugs into a
  pretrained 8B VLM, with deterministic Gaussian centers and an
  uncertainty-aware token budget.  The branch and its training objective
  together transform geometric reconstruction quality into a regularizer
  on the LLM's visual reasoning.

* **A structured manipulation-plan supervision target** organized around a
  five-category × three-role constraint taxonomy and a part-aware
  affordance-hint convention, making model outputs *verifiable predicates*
  rather than free-form text.

* **A 27 K-episode unified data pipeline** spanning twelve heterogeneous
  robotics datasets with mixed native and pseudo depth, together with a
  three-level generalization evaluation protocol (seen / unseen / cross-
  camera) that isolates the contribution of the 3D branch.

* **A cross-embodiment closed-loop evaluation** that executes the typed plans
  through a training-free relational-keypoint-constraint optimizer in two
  simulators of different embodiment — single-arm LIBERO and dual-arm
  RoboTwin — and isolates the frozen planner's perception-transfer cost with a
  privileged-keypoint upper bound, testing view-and-embodiment transfer in
  *execution* rather than only in offline metrics.

* **Open release** of the data pipeline, training and inference code, and
  trained checkpoints, including the LangSAM-based test-time refinement
  used in our ablations.

The remainder of the paper is organized as follows.  §2 reviews 3D-enhanced
VLMs and embodied planning literatures.  §3 details the GaussianBrain
architecture and the joint training objective.  §4 describes the data
pipeline and plan supervision schema.  §5 reports the offline plan-quality
probe, the three-level benchmark and its ablations, the closed-loop
cross-embodiment study, and qualitative analyses.  §6 discusses limitations
(single-frame inputs, dependence on depth quality) and outlines future work
on temporal Gaussian fields and learned constraint verification.
