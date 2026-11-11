import psycopg2

from config.base import db_host, db_port, db_user, db_name, db_password

conn = psycopg2.connect(
    host=db_host,
    port=db_port,
    user=db_user,
    password=db_password,  # 直接使用原始密码
)

with conn.cursor() as c:
    c.execute(f"DROP DATABASE IF EXISTS {db_name}")
    c.execute(f"CREATE DATABASE {db_name}")
