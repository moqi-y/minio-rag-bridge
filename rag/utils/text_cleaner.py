"""
文本清洗工具：移除 PostgreSQL 等存储不接受的字符。

PostgreSQL 的 text 类型不能存储 NUL（\x00），真实文档（PDF、OCR 等）
解析后常含此类控制字符，写入 pgvector 前需清洗。
"""

from __future__ import annotations

from typing import Any, Dict, List

from llama_index.core.schema import BaseNode, Document

# PostgreSQL 不接受 NUL；其余控制字符按需保留或扩展
_INVALID_CHARS = "\x00"


def clean_text(text: str) -> str:
    """清洗单个字符串：去掉 NUL 等非法字符。"""
    if not isinstance(text, str):
        return text
    for ch in _INVALID_CHARS:
        text = text.replace(ch, "")
    return text


def clean_metadata(metadata: Dict[str, Any]) -> Dict[str, Any]:
    """递归清洗 metadata 中的字符串值（含嵌套 dict/list）。"""
    if isinstance(metadata, dict):
        return {clean_text(k): clean_metadata(v) for k, v in metadata.items()}
    if isinstance(metadata, list):
        return [clean_metadata(item) for item in metadata]
    return clean_text(metadata)


def clean_document(doc: Document) -> Document:
    """清洗一个 Document 的 text 和 metadata，原地修改并返回。"""
    doc.set_content(clean_text(doc.text))   # Document.text 只读，用 set_content 修改
    doc.metadata = clean_metadata(doc.metadata)
    return doc


def clean_node(node: BaseNode) -> BaseNode:
    """清洗一个 Node 的 text 和 metadata。"""
    if hasattr(node, "text") and node.text is not None:
        node.set_content(clean_text(node.text))  # 同理，Node 也用 set_content
    node.metadata = clean_metadata(node.metadata)
    return node


def clean_documents(docs: List[Document]) -> List[Document]:
    """批量清洗 Document 列表。"""
    return [clean_document(d) for d in docs]


def clean_nodes(nodes: List[BaseNode]) -> List[BaseNode]:
    """批量清洗 Node 列表。"""
    return [clean_node(n) for n in nodes]


# 示例
# minio_docs = clean_documents(documents)  # 把加载的文档内容进行清洗
# index = VectorStoreIndex.from_documents(
#     minio_docs,
#     storage_context=storage_context,
#     show_progress=True,
# )