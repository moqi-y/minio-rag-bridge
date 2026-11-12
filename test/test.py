from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings

from model.embed_model import OllamaEmbedModel
from model.llm_model import OllamaModel

#  加载文档
documents = SimpleDirectoryReader("../data").load_data()
# 设置嵌入模型
Settings.embed_model = OllamaEmbedModel().get_model()
# 创建向量存储索引
index = VectorStoreIndex.from_documents(documents, show_progress=True)
# 设置检索器（大语言模型）
Settings.llm = OllamaModel()
# 创建查询引擎
query_engine = index.as_query_engine(
    similarity_top_k=3,
    streaming=True,  # 开启流式输出
)
# 查询
if __name__ == '__main__':
    # 流式查询，response 是 StreamingResponse
    response = query_engine.query("将本地分支的更改推送到对应的远程分支的命令")
    # 流式文本
    for chunk in response.response_gen:
        print("流式响应：", chunk, end="", flush=True)
    # 来源信息
    for node in response.source_nodes:
        print("来源：", node.node.metadata, node.score)
