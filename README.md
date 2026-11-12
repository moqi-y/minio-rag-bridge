
# minio-rag-bridge

**把 MinIO 里的文档，变成你 PostgreSQL 里可问答的知识库。**

一套基于 LlamaIndex 的轻量级 RAG 方案：文档留在 MinIO，向量写进你已有的 PostgreSQL（pgvector），不新增向量数据库，不改变现有运维体系。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.13+](https://img.shields.io/badge/python-3.13%2B-blue.svg)](https://www.python.org/downloads/)

---

## 为什么做这个项目

大多数 RAG 教程默认你从零搭建向量库，或者把文档迁移到新的存储系统。但真实场景往往是：**文档已经在 MinIO 里了，数据库已经在跑 PostgreSQL 了。**

`minio-rag-bridge` 的目标很简单：在这两套已有系统之间搭一座桥，让你用最短的路径获得一个可用的私有知识库问答系统，而不必引入 Milvus、Qdrant 等额外的运维负担。

### 它适合谁

- 团队已有 MinIO 对象存储，文档以 PDF / Word / Markdown 等形式存放其中
- 业务系统使用 PostgreSQL，愿意通过 `pgvector` 扩展承载向量数据
- 希望数据不出内网，备份、监控、权限复用现有体系
- 需要来源可追溯的问答（能列出答案引用了哪个文件）

### 它不做什么

- 不替代 MinIO 或 PostgreSQL 的运维
- 不提供复杂的 Agent 编排（那是 LangGraph 的领域）
- 不承诺“开箱即用的完美检索”——检索质量需要通过你的真实数据调优

---

## 架构

**数据流**：MinIO Bucket 中的文档 → `MinioReader` 加载 → LlamaIndex 切分与向量化 → `PGVectorStore` 写入 PostgreSQL → 查询时检索相似片段 → LLM 生成带来源的答案。

---

## 快速开始

### 前置条件

- Python 3.10+
- 可访问的 MinIO 实例（及 Access Key / Secret Key）
- 已启用 `pgvector` 扩展的 PostgreSQL 实例（`CREATE EXTENSION vector;`）
- 注意：Docker 用户：不要用普通的 postgres 镜像，改用官方集成了扩展的镜像`pgvector/pgvector:pg16`，并在业务库`knowledge_base`里执行`CREATE EXTENSION vector;`
### 安装

```bash
# 自动读取 pyproject.toml 和 uv.lock，创建/更新虚拟环境，并安装项目依赖。
uv sync
```

或从源码安装：

```bash
git clone https://github.com/yourname/minio-rag-bridge.git
cd minio-rag-bridge
pip install -e .
```

### 配置

创建 `.env` 文件：

```env
# MinIO
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=your_access_key
MINIO_SECRET_KEY=your_secret_key
MINIO_BUCKET=knowledge-docs
MINIO_PREFIX=docs/              # 可选：只读取某个目录

# PostgreSQL
PG_HOST=localhost
PG_PORT=5432
PG_USER=postgres
PG_PASSWORD=your_password
PG_DATABASE=knowledge_base
PG_TABLE=ai_knowledge_vectors

# Embedding（默认使用 OpenAI，可替换）
OPENAI_API_KEY=sk-...
EMBED_DIM=1536                  # 需与嵌入模型输出维度一致
```

### 构建索引

```python
from minio_rag_bridge import KnowledgeBase

kb = KnowledgeBase.from_env()

# 从 MinIO 加载文档并写入 pgvector
kb.ingest(
    bucket="knowledge-docs",
    prefix="docs/",
)
```

### 查询

```python
response = kb.query("项目的部署流程是什么？")

print(response.text)

# 列出答案引用的来源
for node in response.source_nodes:
    print(f"来源: {node.metadata.get('file_name')} (相关度: {node.score:.3f})")
```

---

## 核心特性

### 文档来源可追溯

每个检索到的节点都携带 MinIO 中的文件元数据。答案附带 `source_nodes`，可列出具体引用了哪个文件、哪个片段，方便验证与审计。

### 混合检索（Hybrid Search）

`PGVectorStore` 支持向量相似度与关键词检索的混合模式。对于包含专有名词、产品型号、法规编号的知识库，混合检索能显著降低“语义相近但事实错误”的召回问题。

```python
kb = KnowledgeBase.from_env(hybrid_search=True)
response = kb.query("ISO 27001 的访问控制要求", vector_store_query_mode="hybrid")
```

### 增量刷新友好

支持基于文档内容哈希的刷新策略：只对 MinIO 中发生变化的文件重新计算向量，避免全量重灌带来的嵌入成本。

### 可替换的嵌入模型

默认使用 OpenAI 嵌入，但通过 LlamaIndex 的 `embed_model` 接口可轻松替换为本地模型（如 BGE 系列），适合对数据出境有要求的场景。

---

## 技术栈

| 组件 | 角色 |
|------|------|
| **MinIO** | 文档源，S3 兼容对象存储 |
| **LlamaIndex** | 文档加载、切分、索引、查询编排 |
| **MinioReader** | LlamaIndex 官方 MinIO 读取器，支持 Bucket / 前缀 / 单文件 |
| **PGVectorStore** | LlamaIndex 官方 PostgreSQL 向量存储集成 |
| **pgvector** | PostgreSQL 向量扩展，支持 HNSW / IVFFlat 索引 |

---

## 路线图

- [x] MinIO Bucket 文档加载与索引
- [x] PostgreSQL/pgvector 向量存储
- [x] 来源引用输出
- [x] 混合检索模式
- [ ] 增量刷新（基于 doc_id + 内容哈希）
- [ ] CLI 工具（`minio-rag ingest` / `minio-rag query`）
- [ ] Docker Compose 本地开发环境
- [ ] 中文嵌入模型配置示例（BGE / BCE）

---

## 贡献

欢迎 Issue 和 PR。在提交之前，请确保：

1. 新增功能附带测试
2. 文档同步更新
3. 不引入新的重型依赖（如新的向量数据库）

---

## 许可证

MIT

---

**minio-rag-bridge** — 让知识库搭建回归“用已有的东西解决问题”。
```