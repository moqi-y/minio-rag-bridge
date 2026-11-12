"""
Postgres 向量操作
"""
from llama_index.vector_stores.postgres import PGVectorStore
from llama_index.core.vector_stores import VectorStoreQuery
from typing import List, Optional, Any
from llama_index.core.schema import BaseNode, TextNode
from sqlalchemy import URL, create_engine
from sqlalchemy.ext.asyncio import create_async_engine

from config.base import db_name, db_host, db_password, db_port, db_user, vector_db_table_name, embedding_model_dim

"""
PGVectorStore 内部会同时管理同步和异步两条连接路径。
它的构造函数逻辑是：要么你提供一对完整的 engine（同步+异步），要么它自己根据连接参数创建。
只给 engine 不给 async_engine，它会认为配置不完整，直接抛 ValueError。
"""


class VectorOps:
    def __init__(self):
        self.vector_store = None

        # 同步 URL
        sync_url = URL.create(
            "postgresql+psycopg2",
            username=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
            database=db_name,
        )
        # 异步 URL（驱动改成 asyncpg）
        async_url = URL.create(
            "postgresql+asyncpg",
            username=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
            database=db_name,
        )
        sync_engine = create_engine(sync_url)
        async_engine = create_async_engine(async_url)

        self.vector_store = PGVectorStore(
            engine=sync_engine,
            async_engine=async_engine,
            table_name=vector_db_table_name,
            embed_dim=int(embedding_model_dim),
        )

    # 返回vector_store对象
    def get_vector_store(self):
        return self.vector_store

    # ------------------------------------------------------------
    # 存储向量：PGVectorStore 实际接收的是节点（Node）
    # ------------------------------------------------------------
    def store_vector(self, node: BaseNode) -> List[str]:
        """
        向 PGVectorStore 添加一个节点。
        node 需要已经包含 embedding 和 metadata。
        如果希望用 vector_name/vector_path 标识，请写入 node.metadata：
            node.metadata["vector_name"] = ...
            node.metadata["vector_path"] = ...
        """
        return self.vector_store.add([node])

    # ------------------------------------------------------------
    # 查询向量：PGVectorStore 的查询是向量相似度检索
    # ------------------------------------------------------------
    def query_vector(self, query_embedding: List[float], top_k: int = 5,
                     filters: Optional[Any] = None):
        """
        基于向量做相似度查询。
        若要按 vector_name/vector_path 过滤，需传入 MetadataFilters。
        """
        query = VectorStoreQuery(
            query_embedding=query_embedding,
            similarity_top_k=top_k,
            filters=filters,
        )
        return self.vector_store.query(query)

    # ------------------------------------------------------------
    # 更新向量：PGVectorStore 没有直接的 update 接口
    # 常见做法是先删除旧节点，再插入新节点
    # ------------------------------------------------------------
    def update_vector(self, ref_doc_id: str, new_node: BaseNode) -> List[str]:
        """
        先按 ref_doc_id 删除旧数据，再写入新节点。
        注意：delete 按 ref_doc_id 删除的是该文档下所有节点。
        """
        self.vector_store.delete(ref_doc_id)
        return self.vector_store.add([new_node])

    # ------------------------------------------------------------
    # 全量更新：本质上就是清空后重新写入
    # ------------------------------------------------------------
    def update_all_vectors(self, nodes: List[BaseNode]) -> List[str]:
        """
        全量覆盖。PGVectorStore 没有专门的“全量更新”方法，
        需要先清空表数据，再批量写入。
        如果表结构也要重建，建议直接 drop table 后重新初始化。
        """
        # 清空方式取决于底层实现；较稳妥的做法是用 SQL 执行 TRUNCATE
        # 这里假设你接受通过底层引擎执行清空操作
        from sqlalchemy import text
        with self.vector_store._engine.connect() as conn:
            conn.execute(text(f"TRUNCATE TABLE {self.vector_store.table_name}"))
            conn.commit()
        return self.vector_store.add(nodes)

    # ------------------------------------------------------------
    # 删除指定向量：按 ref_doc_id 删除（会删掉该文档下所有节点）
    # ------------------------------------------------------------
    def delete_vector(self, ref_doc_id: str):
        """
        PGVectorStore 的 delete 接口只支持按 ref_doc_id 删除。
        如果你用 vector_name/vector_path 标识，需要把 ref_doc_id 设为对应值，
        或者在 metadata 中做过滤后逐个删除。
        """
        self.vector_store.delete(ref_doc_id)

    # ------------------------------------------------------------
    # 删除所有向量：清空表
    # ------------------------------------------------------------
    def delete_all_vectors(self):
        """
        清空 PGVectorStore 对应表的所有数据。
        底层可通过 TRUNCATE 实现，保留表结构。
        """
        from sqlalchemy import text
        with self.vector_store._engine.connect() as conn:
            conn.execute(text(f"TRUNCATE TABLE {self.vector_store.table_name}"))
            conn.commit()


if __name__ == '__main__':
    # 测试向量存储
    vectorOps = VectorOps()
    res = vectorOps.get_vector_store()
    print(res)
