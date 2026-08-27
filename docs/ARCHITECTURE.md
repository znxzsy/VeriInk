# Public demo architecture

VeriInk's public edition keeps the core contract small and inspectable:

```text
case specification
      |
      v
deterministic renderer -----> PNG scene
      |                           |
      +------ label + seed -------+
                                  |
                                  v
                     manifest + integrity checks
```

Every demo image is generated from a fixed case specification and seed. The
manifest records the intended visible answer, transcription, safe ink bounds,
and SHA256 digest. Regenerating the gallery with the same code, fonts, and seed
produces the same pixels.

This repository does **not** include production distributions, real student
images, private datasets, service credentials, internal endpoints, upload
pipelines, proprietary rejection policies, or high-volume orchestration.

