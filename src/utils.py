# src/utils.py - 工具函数
import pandas as pd
import streamlit as st
from config import DATA_PROCESSED

@st.cache_data  # Streamlit缓存装饰器，避免重复加载数据
def load_data(use_processed=True):
    """安全加载CSV数据，自动处理编码错误"""
    path = DATA_PROCESSED if use_processed else DATA_RAW
    try:
        return pd.read_csv(path, encoding="utf-8")
    except FileNotFoundError:
        st.error(f"❌ 数据文件不存在: {path}")
        st.info("💡 请先运行 `src/data_cleaning.py` 生成处理后的数据")
        return None
    except Exception as e:
        st.error(f"❌ 数据加载失败: {e}")
        return None

def save_model(model, path):
    """保存模型到本地"""
    import joblib
    joblib.dump(model, path)
    print(f"✅ 模型已保存至 {path}")

def load_model(path):
    """加载模型，带异常处理"""
    import joblib
    try:
        return joblib.load(path)
    except FileNotFoundError:
        return None