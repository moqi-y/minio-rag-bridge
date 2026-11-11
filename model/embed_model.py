from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.embeddings.openai import OpenAIEmbedding

from config.base import (
    embedding_model_name,
    embedding_model_api_url,
)


class OpenAIEmbedModel:
    """创建并返回 LlamaIndex 可用的 OpenAI 嵌入模型实例。"""

    def __init__(self, model_name=embedding_model_name, api_key=embedding_model_api_url):
        self.model_name = model_name
        self.api_key = api_key
        self._embed_model = None

    def get_model(self) -> OpenAIEmbedding:
        if self._embed_model is None:
            self._embed_model = OpenAIEmbedding(
                model=self.model_name,
                api_key=self.api_key,
            )
        return self._embed_model

    def __str__(self):
        return f"OpenAIEmbedModel-Model Name: {self.model_name}"


class OllamaEmbedModel:
    """创建并返回 LlamaIndex 可用的 Ollama 嵌入模型实例。"""

    def __init__(self, model_name=embedding_model_name, base_url=embedding_model_api_url):
        self.model_name = model_name
        self.base_url = base_url
        self._embed_model = None

    def get_model(self) -> OllamaEmbedding:
        if self._embed_model is None:
            self._embed_model = OllamaEmbedding(
                model_name=self.model_name,
                base_url=self.base_url,
            )
        return self._embed_model

    def __str__(self):
        return f"OllamaEmbedModel-Model Name: {self.model_name}, Base URL: {self.base_url}"


# 使用实例
if __name__ == '__main__':
    # openai_model = OpenAIEmbedModel()
    # print(openai_model)
    # print("  实际维度:", len(openai_model.get_model().get_text_embedding("测试")))

    ollama_model = OllamaEmbedModel()
    print(ollama_model)
    print("  实际维度:", len(ollama_model.get_model().get_text_embedding("测试")))
