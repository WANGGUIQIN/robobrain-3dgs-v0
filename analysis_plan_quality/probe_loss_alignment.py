#!/usr/bin/env python3
"""Probe whether train.py's prompt/label alignment is correct.

Tests for two bugs:
  (A) plen mismatch — prompt-only tokenization differs from prefix of full
      tokenization, causing labels[:plen]=-100 to mask wrong positions.
  (B) padding side bug — if processor pads on the LEFT, labels[:plen]
      mask the start (which is PAD), leaving the actual prompt UNMASKED
      and computed as loss-bearing target.

Output: prints token IDs at [plen-3:plen+3] under both per-sample and
batch (padded) tokenization. If they don't align, loss masking is broken.

Run:
  CUDA_VISIBLE_DEVICES=1 /home/edge/miniconda3/envs/robobrain/bin/python \
    /home/edge/RoboBrain/analysis_plan_quality/probe_loss_alignment.py
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path("/home/edge/RoboBrain/w50037733")
sys.path.insert(0, str(ROOT))

import torch
from PIL import Image
from transformers import AutoProcessor

from utils.prompt_utils import augment_prompt, PLANNING_SYSTEM_PROMPT, DEFAULT_SYSTEM_PROMPT

MODEL = "/home/edge/RoboBrain/models/RoboBrain2.5-8B-NV"
SAMPLE_DIR = Path("/home/edge/RoboBrain/analysis_plan_quality/episodes/01_rlbench_episode_001722")


def synthesize_target_from_plan(plan_path: Path) -> str:
    """Mimic data/unified_loader.py's target construction (just enough for length test)."""
    import json
    p = json.loads(plan_path.read_text())
    out = []
    out.append(f"Scene: {', '.join(p.get('scene_objects', []))}")
    for step in p.get("steps", []):
        out.append(f"Step {step['step']}: {step['action']}({step['target']})")
        h = step.get("affordance_hint", "")
        a = step.get("affordance", [0.5, 0.5])
        out.append(f"  affordance_hint: {h}")
        out.append(f"  affordance: [u={a[0]:.3f}, v={a[1]:.3f}]")
        out.append(f"  done_when: {step.get('done_when','')}")
    out.append("<END_OF_PLAN>")
    return "\n".join(out)


def main() -> None:
    processor = AutoProcessor.from_pretrained(MODEL, trust_remote_code=True)
    tok = processor.tokenizer

    print(f"processor.tokenizer.padding_side = {tok.padding_side!r}")
    print(f"processor.tokenizer.pad_token_id  = {tok.pad_token_id!r}")
    print()

    # Build a 2-sample mini batch with DIFFERENT lengths so padding kicks in
    sys_prompt = DEFAULT_SYSTEM_PROMPT
    user_text_short = augment_prompt("pick up cube", "affordance")
    user_text_long = augment_prompt(
        "this is a deliberately much longer user instruction so the two samples "
        "have different unpadded lengths and we can see what padding does to the "
        "batch tokenization output", "affordance",
    )
    target_short = "Scene: cube\nStep 1: reach(cube)\n  affordance_hint: the red cube\n<END_OF_PLAN>"
    target_long = synthesize_target_from_plan(SAMPLE_DIR / "plan_v2_refined.json")

    img = Image.open(SAMPLE_DIR / "rgb_0.png").convert("RGB").resize((256, 256))

    samples = [
        ("SHORT", user_text_short, target_short),
        ("LONG ", user_text_long,  target_long),
    ]

    # Build full-sequence (prompt+target) text per train.py:447-457
    full_texts = []
    prompt_lens = []  # plen from per-sample tokenization (train.py:496)
    for tag, user_text, target in samples:
        full_msgs = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": [
                {"type": "image", "image": "placeholder"},
                {"type": "text", "text": user_text},
            ]},
            {"role": "assistant", "content": target},
        ]
        full_texts.append(processor.apply_chat_template(full_msgs, tokenize=False, add_generation_prompt=False))

        prompt_msgs = full_msgs[:-1]
        prompt_text = processor.apply_chat_template(prompt_msgs, tokenize=False, add_generation_prompt=True)
        # train.py:492 — per-sample tokenize
        plen = processor(
            text=[prompt_text], images=[img],
            return_tensors="pt", truncation=True, max_length=512,
        )["input_ids"].shape[1]
        prompt_lens.append(plen)

    # Batch tokenize (train.py:464)
    batch = processor(
        text=full_texts, images=[img, img],
        return_tensors="pt", padding=True, truncation=True, max_length=512,
    )
    batch_ids = batch["input_ids"]
    batch_attn = batch["attention_mask"]

    print(f"batch input_ids.shape = {tuple(batch_ids.shape)}")
    print(f"per-sample plen = {prompt_lens}")
    print(f"per-sample real (non-pad) length = {batch_attn.sum(dim=1).tolist()}")
    print()

    for i, (tag, _, target) in enumerate(samples):
        plen = prompt_lens[i]
        ids = batch_ids[i]
        attn = batch_attn[i]
        real_start = (attn == 1).nonzero(as_tuple=True)[0][0].item() if (attn == 1).any() else -1
        real_end = (attn == 1).nonzero(as_tuple=True)[0][-1].item() + 1 if (attn == 1).any() else -1

        print(f"--- sample {i} [{tag}] ---")
        print(f"  plen (per-sample tokenize)              = {plen}")
        print(f"  real-token range in padded batch        = [{real_start}, {real_end})")
        print(f"  real-token length                       = {real_end - real_start}")
        print(f"  pad count at start                      = {real_start}")
        print(f"  expected target start in batch          = {real_start + plen}")
        print(f"  what train.py would mask: labels[:{plen}] = -100")
        print(f"    → covers batch positions [0, {plen})")
        if real_start > 0:
            print(f"    ⚠ but PAD occupies [0, {real_start}); real prompt is at [{real_start}, {real_start + plen})")
            print(f"    ⚠ labels[{plen}:{real_end}] LEAK: includes prompt-tail AND target")

        # Show tokens around the train.py boundary (position plen)
        # And around the TRUE target start (position real_start + plen)
        def decode_window(start: int, width: int = 6) -> str:
            s = max(0, start - width)
            e = min(ids.shape[0], start + width)
            toks = [tok.decode([t.item()]) for t in ids[s:e]]
            return f"[{s}..{e}) " + " | ".join(repr(t) for t in toks)

        print(f"  tokens around labels[:plen] boundary (plen={plen}):")
        print(f"    {decode_window(plen)}")
        print(f"  tokens around TRUE target start ({real_start + plen}):")
        if real_start + plen < ids.shape[0]:
            print(f"    {decode_window(real_start + plen)}")
        else:
            print(f"    (out of range — sequence truncated)")

        # Count how many target tokens survive after train.py masking
        ce_mask = torch.ones_like(ids, dtype=torch.bool)
        ce_mask[:plen] = False                # train.py: labels[:plen] = -100
        ce_mask[attn == 0] = False             # train.py: labels[attn==0] = -100
        n_loss_tokens = ce_mask.sum().item()
        print(f"  → tokens contributing to lm_loss        = {n_loss_tokens}")
        print()

    # Print bottom-line diagnosis
    print("=" * 60)
    if tok.padding_side == "left":
        print("DIAGNOSIS: tokenizer is LEFT-padded.")
        print(f"  train.py:497 'labels[i, :plen] = -100' masks the PAD region")
        print(f"  + a prefix of REAL prompt — NOT the actual prompt boundary.")
        print(f"  This means LOTS of prompt tokens are kept as loss targets,")
        print(f"  and the FINAL target tokens (the planning output) may be ")
        print(f"  CORRECTLY counted as loss — but mixed with prompt tokens.")
        print(f"  The prompt is highly templated → trivially predicted → loss ~ 1e-8.")
    else:
        print("DIAGNOSIS: tokenizer is RIGHT-padded.")
        print(f"  train.py:497 alignment is correct IF prompt-only tokenization")
        print(f"  produces the same prefix as full tokenization.")
        print(f"  Check above whether the tokens at the boundary look like the")
        print(f"  start of the target (e.g. 'Scene:' or similar).")


if __name__ == "__main__":
    main()
