# 3C-AI-Analysis-Tool

# 三创赛AI辅助分析工具

> **项目状态：完成度约七成，已暂停开发。**
> **暂停原因：数据源受限。**
> 三创赛官方不公开结构化的往届获奖数据——获奖名单以网页公示和 PDF 为主，缺少"赛道分类、评分、项目描述"这类可建模字段。仓库里 `data/raw_data/3c_competition_raw.csv` 目前只有 2 条示例记录，仅够跑通流程；要让它真正有用，需要逐届手工整理几百条获奖项目，其成本远高于工具本身的开发成本。三个功能模块均可运行，但结论依赖数据规模，因此暂停在"能跑通、不敢下结论"的状态。

## 项目简介
全国大学生电子商务"创新、创意及创业"挑战赛（三创赛）AI辅助分析工具，基于往届获奖数据，提供赛道趋势分析、项目智能诊断、评分预测三大功能，帮助参赛者科学选题、优化项目。

## 核心功能
1. **赛道趋势分析**：K-Means聚类识别热门赛道，可视化展示获奖分布
2. **项目智能诊断**：TF-IDF提取关键词，对比高分项目给出优化建议
3. **评分预测**：线性回归模型预测得分，支持可解释性分析

## 快速开始

### 环境准备
```bash
# 克隆仓库
git clone https://github.com/IO-zza/3C-AI-Analysis-Tool.git
cd 3C-AI-Analysis-Tool

# 安装依赖
pip install -r requirements.txt
```

也可以用仓库自带的 Dev Container（`.devcontainer/`，Python 3.11）直接打开，依赖需自行安装。

### 运行

```bash
# 1. 清洗数据（生成 data/processed_data/）
python -m src.data_cleaning

# 2. 训练评分模型（生成 models/linear_regression.pkl）
python -m src.score_prediction

# 3. 启动界面
streamlit run app.py
```

`config.py` 中固定了随机种子（42）与测试集比例（0.2），保证结果可复现。

## 目录结构

```
3C-AI-Analysis-Tool/
├── app.py                    Streamlit 主应用（三个标签页）
├── config.py                 路径、随机种子等配置
├── requirements.txt
├── data/
│   └── raw_data/
│       └── 3c_competition_raw.csv   示例数据（2 条，需自行扩充）
├── .devcontainer/            Dev Container 配置
└── src/
    ├── data_cleaning.py      数据清洗
    ├── track_analysis.py     赛道聚类与可视化
    ├── project_diagnosis.py  关键词提取与相似度诊断
    ├── score_prediction.py   模型训练与预测
    └── utils.py              数据 / 模型读写
```

## 数据字段

| 字段 | 说明 |
|---|---|
| 项目名称 | 获奖项目名 |
| 赛道分类 | 如 AI+乡村振兴、跨境电商 |
| 获奖等级 | 一等奖 / 二等奖 / 三等奖 |
| 创新类型 | 技术创新 / 模式创新 / 组合 |
| 市场前景评分 | 0–100 |
| 技术创新评分 | 0–100 |
| 团队实力评分 | 0–100 |
| 核心关键词 | 供 TF-IDF 使用，顿号分隔 |

## 已知限制

1. **数据量**：仅 2 条示例记录，聚类与回归都无法得出有意义的结论。
2. **模型**：线性回归只作基线，特征仅三项评分、样本极少，R² 会剧烈波动，**不具备真正的预测效力**。
3. **诊断**：TF-IDF 余弦相似度反映字面重合度，判断不了商业逻辑，容易把"用词相近"误判成"项目相近"。
4. 因此所有输出只能作为备赛参考，不能替代评委判断，也不构成任何获奖承诺。

## 后续计划

- 数据先行：把公示页面的抓取与结构化做成固定流程，先攒够可分析的样本量
- 诊断换成 LLM 语义检索（向量库 + RAG），替代字符级相似度
- 评分预测按官方评审细则拆成可解释的 rubric，而不是单一总分回归

## License

MIT © 2025 IO-zza
