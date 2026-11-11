from dotenv import load_dotenv
from pathlib import Path
import os

from utils.log_handle import logger

ROOT_DIR = Path(__file__).resolve().parent.parent  # 上溯到项目根目录
env_path = ROOT_DIR / ".env"

# 加载 .env（默认找当前目录）,
load_dotenv(dotenv_path=env_path, override=False)
logger.info("✅加载环境变量成功: {}".format(env_path))

# 大语音模型配置
llm_model_name = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
llm_model_api_key = os.getenv("MODEL_API_KEY", "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
llm_model_api_url = os.getenv("MODEL_API_URL", "https://api.openai.com/v1/chat/completions")

# 嵌入模型配置
embedding_model_name = os.getenv("EMBEDDING_MODEL_NAME", "all-MiniLM-L6-v2")
embedding_model_api_url = os.getenv("EMBEDDING_MODEL_API_URL",
                                    "https://api-inference.huggingface.co/models/all-MiniLM-L6-v2")
embedding_model_api_key = os.getenv("EMBEDDING_MODEL_API_KEY", "hf_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")

# 数据库配置
db_host = os.getenv("DB_HOST", "localhost")
db_port = os.getenv("DB_PORT", "3306")
db_user = os.getenv("DB_USER", "root")
db_password = os.getenv("DB_PASSWORD", "123456")
db_name = os.getenv("DB_NAME", "chatglm")
db_charset = os.getenv("DB_CHARSET", "utf8mb4")
# 向量存储表
vector_db_table_name = os.getenv("VECTOR_DB_TABLE_NAME", "vector_db")

# MinIO配置
minio_endpoint = os.getenv("MINIO_ENDPOINT", "localhost:9000")
minio_access_key = os.getenv("MINIO_ACCESS_KEY", "minio")
minio_secret_key = os.getenv("MINIO_SECRET_KEY", "minio123")
minio_bucket_name = os.getenv("MINIO_BUCKET_NAME", "chatglm")  # 存储桶名称
minio_prefix = os.getenv("MINIO_PREFIX", "/docs")
minio_secure = os.getenv("MINIO_SECURE", "False").lower() in ["true", "1", "yes"]  # 是否使用HTTPS,默认False,即使用HTTP。
