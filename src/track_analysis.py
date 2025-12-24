# src/track_analysis.py - 赛道趋势分析
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
from config import RANDOM_SEED

def analyze_tracks(df, n_clusters=4):
    """K-Means聚类分析赛道热度"""
    # 特征：各赛道平均评分 + 一等奖数量
    track_features = df.groupby("赛道分类").agg({
        "市场前景评分": "mean",
        "技术创新评分": "mean",
        "团队实力评分": "mean",
        "获奖等级": lambda x: (x == "一等奖").sum()
    }).rename(columns={"获奖等级": "一等奖数量"}).reset_index()
    
    # 准备聚类特征
    cluster_features = track_features[["市场前景评分", "技术创新评分", "一等奖数量"]]
    
    # K-Means聚类
    kmeans = KMeans(n_clusters=n_clusters, random_state=RANDOM_SEED, n_init=10)
    track_features["热度等级"] = kmeans.fit_predict(cluster_features)
    
    # 热度等级解读（数值越大越热门）
    track_features["热度等级"] = track_features["热度等级"].map({
        0: "🔥 热门", 1: "⭐ 较热", 2: "📈 潜力", 3: "💡 小众"
    })
    
    return track_features

def plot_track_charts(df):
    """生成赛道分析图表"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # 图1：获奖数量分布
    track_counts = df["赛道分类"].value_counts()
    sns.barplot(x=track_counts.index, y=track_counts.values, 
                ax=axes[0,0], palette="Set2")
    axes[0,0].set_title("各赛道获奖项目数量", fontsize=13)
    axes[0,0].tick_params(axis='x', rotation=45)
    
    # 图2：平均评分对比
    track_avg = df.groupby("赛道分类")[["市场前景评分", "技术创新评分"]].mean()
    track_avg.plot(kind='bar', ax=axes[0,1], color=['#1f77b4', '#ff7f0e'])
    axes[0,1].set_title("赛道平均评分对比", fontsize=13)
    axes[0,1].tick_params(axis='x', rotation=45)
    
    # 图3：评分相关性
    sns.scatterplot(data=df, x="市场前景评分", y="技术创新评分", 
                    hue="赛道分类", ax=axes[1,0], alpha=0.7)
    axes[1,0].set_title("市场前景 vs 技术创新", fontsize=13)
    
    # 图4：总分分布
    sns.histplot(df["总分"], bins=20, kde=True, ax=axes[1,1], color='green')
    axes[1,1].set_title("项目总分分布", fontsize=13)
    
    plt.tight_layout()
    return fig