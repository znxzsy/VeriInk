<p align="right"><strong>English</strong> · <a href="RSI_WORKFLOW_ZH.md">中文</a></p>

# RSI workflow: verifiable synthesis

VeriInk supplies controlled practice examples to an externally managed improvement loop. Its public executable scope is seeded rendering plus artifact validation.

## Concrete handoff

- Input: a manually reviewed requirement, `SlotSpec` values and a seed.
- Generate: run `python scripts/generate_demo.py` for the public synthetic gallery.
- Inspect: `examples/gallery/manifest.json` records page paths, seeds, visible answers, transcriptions, checks and image hashes. `verify_gallery` checks the stored contract; visual review remains necessary.
- Hand off: a domain adapter can convert selected images and externally supplied grader outputs into AlignLedger's documented import format. This mapping is not bundled; do not assume the two manifest schemas are interchangeable.
- Consume: an external process freezes the training selection and separately evaluates the resulting model. The renderer does not select checkpoints.

## Decisions and evidence

1. Keep review/discovery data and evaluation data separate. Define source/group split rules before training; these repositories do not enforce research-wide leakage checks.
2. Preserve unknown and rejected cases. A model failure can indicate missing practice, ambiguous evidence or a data error; it does not automatically justify changing the generator.
3. Retaining a valid data capability and adopting a trained checkpoint are separate decisions. Hashes and passing software tests establish neither model improvement nor real-world transfer.
4. Compare against a fixed baseline under a declared budget, preserve negative results, and evaluate on an appropriately isolated set before promotion.

## Public release boundary

This is a human-guided data workflow. No automatic connection between the two repositories, recursive trainer, autonomous code-generation agent, research verifier or model-promotion controller is shipped here. The illustrative record below has no operational authority and is not an experimental receipt. Core research code, prompts, private data and model weights stay outside these repositories.

## Illustrative bookkeeping

See [rsi_round.example.json](../examples/rsi_round.example.json). Every entry is invented. Pending evaluation must stay pending; it is not a failed experiment or a successful promotion.
