import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from config import DATA_RAW, DATA_PROCESSED, DATA_PROCESSED_DIR

def clean_data():
    """清洗原始数据：去重、填充缺失值、标准化"""
    print("📥 正在读取原始数据...")
    df = pd.read_csv(DATA_RAW, encoding="utf-8")
    print(f"原始数据量: {len(df)} 条")
    
    # 1. 去重
    df.drop_duplicates(inplace=True)
    print(f"去重后: {len(df)} 条")
    
    # 2. 统一赛道名称（去除空格、全角符号）
    df["赛道分类"] = df["赛道分类"].str.strip().str.replace(" ", "")
    
    # 3. 填充评分缺失值（用中位数，避免异常值影响）
    score_cols = ["市场前景评分", "技术创新评分", "团队实力评分"]
    for col in score_cols:
        missing_count = df[col].isna().sum()
        if missing_count > 0:
            median_val = df[col].median()
            df[col].fillna(median_val, inplace=True)
            print(f"填充 `{col}` 缺失值 {missing_count} 个 → 中位数: {median_val}")
    
    # 4. 核心关键词标准化（转为小写列表）
    df["核心关键词"] = df["核心关键词"].apply(
        lambda x: [kw.strip().lower() for kw in str(x).split("、")] if pd.notna(x) else []
    )
    
    # 5. 创建总分字段（用于模型训练）
    df["总分"] = df[score_cols].mean(axis=1)
    
    # 6. 保存清洗后数据
# DATA_PROCESSED_DIR.mkdir(exist_ok=True)  # 注释掉，云端自动创建
    df.to_csv(DATA_PROCESSED, index=False, encoding="utf-8")
    print(f"\n✅ 数据清洗完成！保存至: {DATA_PROCESSED}")
    print(f"最终数据量: {len(df)} 条")

if __name__ == "__main__":
    clean_data()