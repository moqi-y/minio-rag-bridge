#  官方读取器：MinioReader

from llama_index.readers.minio import MinioReader

from config.base import minio_endpoint, minio_access_key, minio_secret_key, minio_bucket_name, minio_prefix, \
    minio_secure

# 配置 MinioReader
loader = MinioReader(
    minio_endpoint=minio_endpoint,  # 替换为你的 MinIO 地址
    minio_access_key=minio_access_key,
    minio_secret_key=minio_secret_key,
    bucket=minio_bucket_name,
    prefix=minio_prefix,  # 可选：只读取某个目录下的文件
    minio_secure=minio_secure  # 是否使用 HTTPS
)

# 对外暴露使用
documents = loader.load_data()

# 使用 MinioReader 加载数据示例
if __name__ == '__main__':
    print(documents)
