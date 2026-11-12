"""
数据库连接封装
@description: 初始化项目数据库，重建数据库
"""
import psycopg2

from psycopg2 import sql
from config.base import db_host, db_port, db_user, db_name, db_password
from utils.log_handle import logger

# 显式连接到管理库 postgres，避免连到待删除的库本身
conn = psycopg2.connect(
    host=db_host,
    port=db_port,
    user=db_user,
    password=db_password,
)

# 关键：开启自动提交，否则 DROP/CREATE DATABASE 会报事务块错误
conn.autocommit = True

try:
    with conn.cursor() as c:
        # 用 sql.Identifier 安全地引用数据库名，避免特殊字符/注入问题
        c.execute(sql.SQL("DROP DATABASE IF EXISTS {}").format(sql.Identifier(db_name)))
        c.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
    logger.info("数据库重建成功")
finally:
    conn.close()

if __name__ == '__main__':
    logger.info("数据库连接成功")
