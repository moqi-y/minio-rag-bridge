import requests
from typing import Any, Generator
from llama_index.core.llms import CustomLLM, CompletionResponse, LLMMetadata
from llama_index.core.llms.callbacks import llm_completion_callback
from llama_index.llms.ollama import Ollama

from config.base import llm_model_name, llm_model_api_url, llm_model_api_key


class OpenAIModel(CustomLLM):
    """封装自定义 OpenAI 兼容 LLM，适配 LlamaIndex 调用。"""

    model_name: str = llm_model_name
    api_key: str = llm_model_api_key
    api_url: str = llm_model_api_url

    @property
    def metadata(self) -> LLMMetadata:
        return LLMMetadata(
            model_name=self.model_name,
            context_window=3900,
            num_output=1024,
            is_chat_model=True,
        )

    @llm_completion_callback()
    def complete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": kwargs.get("temperature", 0.7),
        }
        resp = requests.post(self.api_url, json=payload, headers=headers, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        text = data["choices"][0]["message"]["content"]
        return CompletionResponse(text=text)

    @llm_completion_callback()
    def stream_complete(self, prompt: str, **kwargs: Any):
        # 如果需要流式输出，可在此实现；查询引擎非流式场景下不会调用此方法
        response = self.complete(prompt, **kwargs)
        yield CompletionResponse(text=response.text, delta=response.text)


class OllamaModel(Ollama):
    """直接继承 LlamaIndex 的 Ollama，可赋值给 Settings.llm。"""

    def __init__(self, model_name=llm_model_name, api_url=llm_model_api_url):
        super().__init__(
            model=model_name,
            base_url=api_url,
            request_timeout=120.0,
        )

    def __str__(self):
        return f"OllamaModel-Model: {self.model}, Base URL: {self.base_url}"


# 使用实例
if __name__ == "__main__":
    from llama_index.core import Settings

    Settings.llm = OllamaModel()
    # 非流式调用
    # resp = Settings.llm.complete("用一句话解释 RAG")
    # print(resp)

    # 流式调用
    for chunk in Settings.llm.stream_complete("用一句话解释 RAG"):
        print(chunk.delta, end="", flush=True)
