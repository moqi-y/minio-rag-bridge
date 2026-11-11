from dotenv import load_dotenv
from pathlib import Path
import os

ROOT_DIR = Path(__file__).resolve().parent.parent  # 上溯到项目根目录
env_path = ROOT_DIR / ".env"

# 加载 .env（默认找当前目录）,
load_dotenv(dotenv_path=env_path, override=False)
print(os.getenv("MINIO_ENDPOINT", ''))

# 大语音模型配置
llm_model_name = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
llm_model_api_key = os.getenv("MODEL_API_KEY", "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
llm_model_api_url = os.getenv("MODEL_API_URL", "https://api.openai.com/v1/chat/completions")

# 嵌入模型配置
embedding_model_name = os.getenv("EMBEDDING_MODEL_NAME", "all-MiniLM-L6-v2")
embedding_model_api_url = os.getenv("EMBEDDING_MODEL_API_URL","https://api-inference.huggingface.co/models/all-MiniLM-L6-v2")
embedding_model_api_key = os.getenv("EMBEDDING_MODEL_API_KEY", "hf_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
