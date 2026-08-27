<p align="right"><a href="README.md">English</a> · <strong>中文</strong></p>

<p align="center"><img src="assets/hero.png" alt="VeriInk 可验证手写仿真引擎" width="100%" /></p>

# VeriInk

模型刚做错的题，往往正是下一轮最缺的数据。VeriInk 根据失败样本生成一批同类型手写题，把 seed、可见答案、目标转写、笔迹边界和文件哈希一并记录下来。检查不通过的样本不会进入训练集。

公开版保留了容易核验的部分：确定性渲染、故意写错、涂改重写和明确的 manifest。它可以用于 OCR、多模态批改、后训练和回归评测。

## 工作流程

<p align="center"><img src="assets/method_overview.svg" alt="VeriInk 工作流程" width="100%" /></p>

模型错误决定下一批数据做什么。系统先把错误整理成题目规格，再生成可控的手写场景，检查标签、像素边界和文件完整性。通过检查的样本可以进入训练或回归；以后出现问题，也能用 seed 重建并追到原始生成记录。

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
