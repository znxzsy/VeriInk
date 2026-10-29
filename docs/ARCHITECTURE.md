<p align="right"><strong>English</strong> · <a href="ARCHITECTURE_ZH.md">中文</a></p>

# Public demo architecture

The public edition keeps a small, inspectable data contract: a fixed specification and seed enter the deterministic renderer, which produces an image, labels, coordinates, and a file hash for validation.

```text
specification + seed
          |
          v
deterministic renderer -----> image
          |                       |
          +-- labels + bounds ----+
                                  |
                                  v
                     manifest + integrity checks
```

The same code, fonts, specification, and seed reproduce the same pixels. The manifest stores visible answers, target transcriptions, labels, safe ink bounds, and SHA256 digests.

The public repository excludes production distributions, real student images, private datasets, service credentials, internal endpoints, upload pipelines, proprietary rejection policies, and high-volume orchestration.

## RSI handoff

[Workflow and external responsibilities](RSI_WORKFLOW.md)
