import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import joblib
from config import RANDOM_SEED, TEST_SIZE, MODEL_PATH, DATA_PROCESSED, DATA_RAW
from src.utils import save_model
def train_model():
    """训练线性回归模型并评估"""
    print("📊 加载处理后的数据...")
    df = pd.read_csv(DATA_PROCESSED)
    # 特征和标签
    feature_cols = ["市场前景评分", "技术创新评分", "团队实力评分"]
    X = df[feature_cols]
    y = df["总分"]
    
    # 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_SEED
    )
    print(f"训练集: {len(X_train)} 条, 测试集: {len(X_test)} 条")
    
    # 训练模型
    model = LinearRegression()
    model.fit(X_train, y_train)
    print("🤖 模型训练完成！")
    
    # 评估
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"\n📈 模型评估指标:")
    print(f"  - 均方误差 (MSE): {mse:.2f}")
    print(f"  - 决定系数 (R²): {r2:.2f} (越接近1越好)")
    
    # 特征重要性
    print(f"\n🔍 特征权重:")
    for col, coef in zip(feature_cols, model.coef_):
        print(f"  - {col}: {coef:.2f}")
    
    # 保存模型
    save_model(model, MODEL_PATH)
    return model

def predict_score(model, market_score, tech_score, team_score):
    """预测单个项目评分"""
    input_data = [[market_score, tech_score, team_score]]
    prediction = model.predict(input_data)[0]
    return round(prediction, 1)

if __name__ == "__main__":
    from config import DATA_PROCESSED
    train_model()