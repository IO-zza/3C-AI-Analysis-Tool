# 3C-AI-Analysis-Tool

# 三创赛AI辅助分析工具

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
git clone https://github.com/你的用户名/3C-AI-Analysis-Tool.git
cd 3C-AI-Analysis-Tool

# 安装依赖
pip install -r requirements.txt