<p align="right"><a href="README.md">English</a> · <strong>中文</strong></p>

<p align="center"><img src="assets/hero.png" alt="VeriInk 可验证手写仿真引擎" width="100%" /></p>

# VeriInk

**VeriInk 是面向反馈驱动模型迭代与 RSI 研究的可验证合成层。** 经复核的模型失败案例用于设计下一批可控手写任务；公开渲染器记录 seed、可见答案、目标转写、笔迹边界和文件哈希，让每个合成样本可以重建和检查。

公开版保留了容易核验的部分：确定性渲染、故意写错、涂改重写和明确的 manifest。它可以用于 OCR、多模态批改、后训练和回归评测。

## 在 RSI 中负责什么

这里的 RSI 指递归自改进：上一轮的证据用于指导下一轮。VeriInk 提供可控合成练习，[AlignLedger](https://github.com/znxzsy/AlignLedger) 提供人工复核与可追溯反馈；训练和独立评测将这些数据工具连接到研究闭环。

| 环节 | 公开版支持 | 能力边界 |
| --- | --- | --- |
| 分析已复核失败案例 | 人工编写任务规格 | 未包含自主诊断 Agent |
| 生成相关练习 | 固定 seed、错误作答与划改渲染 | 基于公开版现有任务库 |
| 检查合成产物 | 渲染意图、边界和 SHA256 检查 | 仍需视觉语义复核 |
| 复核并冻结数据 | 提供 AlignLedger 交接说明 | 接入仍需领域适配器 |
| 训练、比较并回流 | 提供研究流程说明 | 训练与模型晋升由外部流程负责 |

[RSI 流程与限制](docs/RSI_WORKFLOW_ZH.md) · [English](docs/RSI_WORKFLOW.md) · [虚构轮次记录](examples/rsi_round.example.json)

<p align="center"><img src="assets/rsi_workflow.svg" alt="RSI 概念流程及公开仓库边界" width="100%" /></p>

更完整的研究已执行训练与评测迭代，以及三种子合成数据采样试跑；该试跑尚未证明自适应采样优势。独立验证的能力扩展和真实场景迁移仍待补齐。公开演示不包含这些实验的完整复现材料。

## 工作流程

<p align="center"><img src="assets/method_overview.svg" alt="VeriInk 工作流程" width="100%" /></p>

图中展示研究流程：维护者把已复核错误整理成任务规格；公开演示负责渲染，并检查渲染意图、笔迹边界和文件完整性。人工复核、训练、回归与晋升分别完成。复现需要相同代码、字体、依赖、规格和 seed。

## 仿真难例

<p align="center"><img src="assets/synthetic_hardcases_cvpr.png" alt="六张仿真手写难例" width="100%" /></p>

这组样例包含涂改重写、小数计算、较大数运算和混合运算比较。六张图都由仿真引擎生成，不含真实学生图片。文件哈希见 [`examples/hardcases/manifest.json`](examples/hardcases/manifest.json)。

## 可复现审查集

<p align="center"><img src="examples/gallery/synthetic_review_wall.png" alt="包含十六个场景的仿真数据审查墙" width="100%" /></p>

演示脚本一次生成 **16 张页面、80 个作答区域**，覆盖基础计算、小数、填空、比较、单位换算、故意写错和涂改重写。[`manifest.json`](examples/gallery/manifest.json) 保存每张图对应的 seed、标签、边界和 SHA256。

学生写错时，数据会保留错法。这样才能训练模型忠实转写，而不是看到题目后自行计算。笔迹出框、标签不一致或文件被修改，验收都会直接失败。

## 快速开始

```bash
git clone https://github.com/znxzsy/VeriInk.git
cd VeriInk
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
python scripts/generate_demo.py
pytest -q
```

命令会重建公开样例、主图、难例墙、审查墙和 manifest，并在结束前重新计算全部哈希。

## 公开范围

仓库只包含仿真演示数据，不含真实学生数据、生产采样分布、内部服务地址、对象存储路径、私有配置、部署脚本、训练集或模型权重。完整边界见 [SECURITY_ZH.md](SECURITY_ZH.md)。

## 合作

完整版本可按具体题型扩展生成规则和质量门禁，也可以接入基座训练、后训练与回归评测。合作或私有化需求请联系微信 **`znxzsy`**。
