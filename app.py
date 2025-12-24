# app.py - Streamlit主应用
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from src.utils import load_data, load_model
from src.track_analysis import analyze_tracks, plot_track_charts
from src.score_prediction import predict_score
from src.project_diagnosis import diagnose_project
from config import MODEL_PATH

# 页面配置
st.set_page_config(
    page_title="三创赛AI辅助分析工具",
    page_icon="🏆",
    layout="wide"
)

st.title("🏆 三创赛AI辅助分析工具")
st.caption("全国大学生电子商务三创赛智能辅助决策系统 | 基于机器学习的数据驱动分析")
st.divider()

# 侧边栏
with st.sidebar:
    st.header("📋 使用指南")
    st.info("""
    1. 准备数据：上传往届获奖数据
    2. 查看趋势：分析赛道热度
    3. 项目诊断：输入项目描述
    4. 评分预测：输入维度评分
    """)
    st.caption("v1.0 | AI课程期末项目")

# 加载数据
df = load_data()
if df is None:
    st.error("❌ 数据加载失败！请确保已运行数据清洗脚本")
    st.stop()

# 标签页布局
tab1, tab2, tab3 = st.tabs(["📊 赛道趋势分析", "🔍 项目智能诊断", "🎯 评分预测"])

# Tab 1: 赛道趋势
with tab1:
    st.subheader("赛道趋势与热度分析")
    with st.spinner("正在分析赛道数据..."):
        track_features = analyze_tracks(df)
        fig = plot_track_charts(df)
        st.pyplot(fig, use_container_width=True)
    
    # 热度等级说明
    st.divider()
    st.caption("🔥 热度等级说明：基于获奖数量+平均评分聚类生成")

# Tab 2: 项目诊断
with tab2:
    st.subheader("项目智能诊断与优化建议")
    project_text = st.text_area(
        "请输入你的项目简介（建议200字以上，包含技术方案、市场分析、团队优势）",
        height=200,
        placeholder="示例：我们的项目是一个基于AI的农产品质量检测平台，使用计算机视觉技术识别果蔬瑕疵，目标客户是大型批发商..."
    )
    
    if st.button("🚀 开始诊断", type="primary"):
        if len(project_text) < 20:
            st.warning("⚠️ 项目描述太短，请详细说明项目亮点")
        else:
            with st.spinner("正在分析项目文本..."):
                result = diagnose_project(project_text, df)
            
            # 结果展示
            col1, col2 = st.columns(2)
            with col1:
                st.metric("与高分项目相似度", f"{result['相似度']:.2f}")
            with col2:
                st.metric("关键词数量", len(result['关键词']))
            
            st.success(f"**诊断结果**: {result['建议']}")
            st.warning(f"**风险提示**: {result['风险提示']}")
            st.write(f"**核心关键词**: {', '.join(result['关键词'])}")

# Tab 3: 评分预测
with tab3:
    st.subheader("项目评分预测与可解释性分析")
    col1, col2, col3 = st.columns(3)
    with col1:
        market_score = st.slider("市场前景评分", 0, 100, 80, help="市场规模、需求迫切性")
    with col2:
        tech_score = st.slider("技术创新评分", 0, 100, 85, help="技术先进性、创新性")
    with col3:
        team_score = st.slider("团队实力评分", 0, 100, 75, help="成员背景、项目经验")
    
    if st.button("🔮 生成预测评分", type="primary"):
        model = load_model(MODEL_PATH)
        if model is None:
            st.error("❌ 预测模型不存在！请先运行 `src/score_prediction.py` 训练模型")
        else:
            prediction = predict_score(model, market_score, tech_score, team_score)
            
            # 结果展示
            st.balloons()
            st.success(f"## 🎯 预测总评分: **{prediction}** / 100")
            
            # 可解释性分析
            st.divider()
            st.write("### 评分构成分析")
            total = market_score + tech_score + team_score
            weights = {
                "市场前景": market_score / total,
                "技术创新": tech_score / total,
                "团队实力": team_score / total
            }
            
            for aspect, weight in weights.items():
                st.progress(weight, text=f"{aspect}: {weight:.1%}")

# 底部信息
st.divider()
st.caption("© 2024 三创赛AI辅助分析工具 | 仅供学习交流使用")