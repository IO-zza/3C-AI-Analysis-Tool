# config.py - 项目配置管理中心
from pathlib import Path

# 项目根目录
BASE_DIR = Path(__file__).resolve().parent

# 数据路径（都用相对路径）
DATA_RAW = BASE_DIR / "data" / "raw_data" / "3c_competition_raw.csv"
DATA_PROCESSED = BASE_DIR / "data" / "processed_data" / "3c_competition_processed.csv"

# 模型路径
MODEL_DIR = BASE_DIR / "models"
MODEL_PATH = MODEL_DIR / "linear_regression.pkl"

# 模型参数（固定随机种子，保证结果可复现）
RANDOM_SEED = 42
TEST_SIZE = 0.2  # 20%数据用于测试