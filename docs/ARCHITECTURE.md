# 公开版架构 / Public Demo Architecture

VeriInk 公开版保留一条精简、可检查的数据契约：固定规格与 seed 进入确定性渲染器，得到图像、标签、坐标和文件哈希，再由验收器统一检查。

The public edition keeps a small, inspectable data contract: a fixed specification and seed enter the deterministic renderer, which produces the image, labels, coordinates, and file hash for validation.

```text
规格与 seed / specification + seed
                  |
                  v
确定性渲染 / deterministic renderer -----> 图像 / image
                  |                           |
                  +---- 标签与坐标 -----------+
                       labels + bounds        |
                                              v
                                manifest + integrity checks
```

同一份代码、字体、规格和 seed 会生成相同像素。manifest 保存可见答案、目标转写、标签、笔迹安全边界和 SHA256。

The same code, fonts, specification, and seed reproduce the same pixels. The manifest stores visible answers, target transcriptions, labels, safe ink bounds, and SHA256 digests.

公开仓库不包含生产数据分布、真实学生图片、私有数据集、服务凭证、内部地址、上传流程、私有拒绝策略或大规模调度代码。

The public repository excludes production distributions, real student images, private datasets, service credentials, internal endpoints, upload pipelines, proprietary rejection policies, and high-volume orchestration.
