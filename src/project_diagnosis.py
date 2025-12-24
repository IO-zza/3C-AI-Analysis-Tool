# src/project_diagnosis.py - 项目诊断
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd

def extract_keywords(text, top_n=10):
    """提取关键词（TF-IDF + 词频）"""
    # 精确模式分词
    words = list(jieba.cut(text))
    
    # 过滤停用词（简单版）
    stopwords = {"的", "了", "和", "是", "在", "有", "我", "你", "他", "它", "们"}
    keywords = [w for w in words if len(w) > 1 and w not in stopwords and not w.isdigit()]
    
    # 统计词频
    from collections import Counter
    word_counts = Counter(keywords)
    return [w for w, _ in word_counts.most_common(top_n)]

def diagnose_project(project_text, df):
    """
    诊断项目：与一等奖项目对比
    project_text: 用户输入的项目描述
    df: 清洗后的数据框
    """
    if len(project_text) < 10:
        return {"error": "项目描述太短"}
    
    # 获取一等奖项目描述
    high_score_projects = df[df["获奖等级"] == "一等奖"]["项目名称"].tolist()
    if not high_score_projects:
        high_score_projects = ["人工智能创新项目", "区块链应用平台"]  # 备用模板
    
    # TF-IDF向量化
    try:
        vectorizer = TfidfVectorizer(tokenizer=jieba.cut, max_features=100)
        corpus = high_score_projects + [project_text]
        tfidf_matrix = vectorizer.fit_transform(corpus)
        
        # 计算余弦相似度
        similarities = cosine_similarity(
            tfidf_matrix[-1],  # 当前项目
            tfidf_matrix[:-1]  # 高分项目
        )
        avg_similarity = float(np.mean(similarities))
    except:
        avg_similarity = 0.5
    
    # 生成建议
    if avg_similarity > 0.6:
        suggestion = "✅ 项目创新点与高分项目相似度较高！建议突出差异化竞争优势"
        risk = "⚠️ 避免与现有项目同质化"
    elif avg_similarity > 0.4:
        suggestion = "⭐ 项目有一定创新性。建议加强技术深度和市场数据支撑"
        risk = "📊 补充市场规模、用户调研等量化分析"
    else:
        suggestion = "💡 项目差异化明显。建议参考高分项目的逻辑结构和表达方式"
        risk = "📝 优化商业计划书撰写规范"
    
    return {
        "相似度": round(avg_similarity, 2),
        "建议": suggestion,
        "风险提示": risk,
        "关键词": extract_keywords(project_text, 8)
    }