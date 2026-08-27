<p align="right"><strong>English</strong> · <a href="README_ZH.md">中文</a></p>

<p align="center"><img src="assets/hero.png" alt="VeriInk: verifiable handwriting synthesis" width="100%" /></p>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.9%2B-356A9A" />
  <img alt="Synthetic data only" src="https://img.shields.io/badge/Data-Synthetic%20Only-2E7D5B" />
  <img alt="Deterministic rendering" src="https://img.shields.io/badge/Rendering-Deterministic-495B72" />
</p>

**VeriInk turns model failures into reproducible handwriting data.** A failed case becomes a controlled batch of related worksheets. The renderer records the seed, visible answer, target transcription, ink bounds, and file hash. Samples that fail the checks never enter the training batch.

The public edition focuses on the part that is easy to audit: deterministic rendering, intentional mistakes, crossed-out revisions, and an explicit manifest. It is designed for OCR, multimodal grading, post-training, and regression evaluation.

## Method

<p align="center"><img src="assets/method_overview.svg" alt="VeriInk method overview" width="100%" /></p>

The model's errors define the next data slice. VeriInk converts those errors into task specifications, renders controlled handwriting scenes, checks label and pixel consistency, and sends accepted samples to training or regression. A later failure can be reproduced from its seed and traced back to the exact generation record.

## Synthetic hard cases

<p align="center"><img src="assets/synthetic_hardcases_cvpr.png" alt="Six synthetic handwriting hard cases" width="100%" /></p>

These examples cover crossed-out revisions, decimal arithmetic, larger-number operations, and mixed-operation comparison. All six images came from the simulator. No real student image is included. Their public hashes are listed in [`examples/hardcases/manifest.json`](examples/hardcases/manifest.json).

## Reproducible audit set

<p align="center"><img src="examples/gallery/synthetic_review_wall.png" alt="Synthetic data audit wall with sixteen verified scenes" width="100%" /></p>

The demo generates **16 pages and 80 answer regions** in one run. It includes arithmetic, decimals, fill-in-the-blank questions, comparisons, unit conversion, intentional mistakes, and crossed-out revisions. [`manifest.json`](examples/gallery/manifest.json) links every image to its seed, labels, bounds, and SHA256.

Wrong answers stay wrong. This is deliberate: a transcription model should copy the visible response instead of correcting it. Out-of-bounds ink, a broken label contract, or a modified file fails validation.

## Quick start

```bash
git clone https://github.com/znxzsy/VeriInk.git
cd VeriInk
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
python scripts/generate_demo.py
pytest -q
```

The command rebuilds the examples, hero image, hard-case plate, audit wall, and manifests. It recomputes every hash before it exits.

## Repository layout

```text
VeriInk/
├── src/veriink/          # deterministic renderer and validation
├── scripts/              # one-command public demo build
├── examples/gallery/     # reproducible audit set
├── examples/hardcases/   # synthetic hard cases and hashes
├── assets/fonts/         # open fonts and licenses
├── tests/                # determinism and input checks
└── docs/                 # architecture and data boundary
```

## Public release boundary

The repository contains synthetic demo data only. It excludes real student data, production distributions, internal endpoints, object-storage paths, private configuration, deployment scripts, training sets, and model weights. See [SECURITY.md](SECURITY.md).

## Collaboration

The full system can be adapted to domain-specific tasks, scaled for data generation and quality gates, and connected to pre-training, post-training, or regression evaluation. For collaboration or private deployment, contact WeChat **`znxzsy`**.

## Data and license

All gallery and hard-case images are synthetic. Bundled fonts remain under their respective SIL Open Font License files. No license is granted for the remaining repository content unless stated otherwise.
