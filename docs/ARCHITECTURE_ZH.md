<p align="right"><a href="ARCHITECTURE.md">English</a> · <strong>中文</strong></p>

# 公开版架构

固定规格与 seed 进入确定性渲染器，得到图像、标签、坐标和文件哈希，再由验收器统一检查。

```text
规格 + seed
    |
    v
确定性渲染器 ------> 图像
    |                 |
    +-- 标签与坐标 ---+
                      |
                      v
                manifest + 完整性检查
```

同一份代码、字体、规格和 seed 会生成相同像素。manifest 保存可见答案、目标转写、标签、笔迹安全边界和 SHA256。

公开仓库不包含生产数据分布、真实学生图片、私有数据集、服务凭证、内部地址、上传流程、私有拒绝策略或大规模调度代码。

## RSI handoff

[交接流程及外部职责](RSI_WORKFLOW_ZH.md)
