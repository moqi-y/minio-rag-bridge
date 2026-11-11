""" rag 入口文件 """
from llama_index.core import VectorStoreIndex, Settings, StorageContext

from model.embed_model import OllamaEmbedModel
from model.llm_model import OllamaModel
from rag.loaders.minio_loader import documents
from rag.storage.vector_ops import VectorOps

# 1、使用minio读取器加载文档
minio_docs = documents

# 2、解析文档，设置嵌入模型
Settings.embed_model = OllamaEmbedModel().get_model()

# 存储向量索引
""" 计划使用pg表存储"""
vectorOps = VectorOps()  # 向量存储操作类
storage_context = StorageContext.from_defaults(vector_store=vectorOps.get_vector_store())

# 3、创建向量存储索引
index = VectorStoreIndex.from_documents(minio_docs, storage_contex=storage_context, show_progress=True)

# 5、设置检索器（大语言模型）
Settings.llm = OllamaModel()

# 6、创建查询引擎
query_engine = index.as_query_engine(
    similarity_top_k=3,  # 相似度最高的k个结果
    streaming=True,  # 开启流式输出
)


# 7、查询返回结果

def query(prompt: str = "将本地分支的更改推送到对应的远程分支的命令"):
    response = query_engine.query(prompt)
    for chunk in response.response_gen:
        yield chunk


if __name__ == '__main__':
    for chunk in query():
        print(chunk, end='', flush=True)
