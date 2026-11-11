import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
LOG_FILE = ROOT_DIR / "logs" / "app.log"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)  # 先建目录

logger = logging.getLogger("system_logger")
logger.setLevel(logging.DEBUG)
logger.propagate = False  # 防止重复打印

if not logger.handlers:  # 防重复添加
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # 控制台处理器
    console_handler = logging.StreamHandler()
    # 控制台日志级别设置
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 文件处理器（只用 RotatingFileHandler，删掉普通 FileHandler）问题1
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=1024 * 1024 * 10,  # 10MB
        backupCount=5,
        encoding="utf-8",  # 问题6
    )
    file_handler.setLevel(logging.DEBUG)  # 问题2
    file_handler.setFormatter(formatter)  # 问题2
    logger.addHandler(file_handler)

if __name__ == "__main__":
    logger.info("This is an info message")
    logger.warning("This is a warning message")
