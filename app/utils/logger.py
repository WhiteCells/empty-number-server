import logging
import queue
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler, QueueHandler, QueueListener
from pathlib import Path
from app.config import Config

log_queue = queue.Queue(-1)

def setup_logger(
    log_dir: str = Config.LOG_DIR,
    level: int = Config.LOG_LEVEL,
    backup_count: int = Config.LOG_BACKUP_COUNT,
    fmt: str = Config.LOG_FORMAT,
) -> logging.Logger:
    """
    异步日志记录器设置
    支持每天一个文件
    自动轮转
    后台写入
    """
    logger = logging.getLogger("app_logger")
    logger.setLevel(level)
    logger.propagate = False 

    if logger.handlers:
        return logger

    Path(log_dir).mkdir(parents=True, exist_ok=True)

    time_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S_%f")
    log_path = Path(log_dir) / f"{time_str}.log"

    formatter = logging.Formatter(fmt)

    file_handler = TimedRotatingFileHandler(
        filename=log_path,
        when="midnight",
        interval=1,
        backupCount=backup_count,
        encoding="utf-8",
        utc=False,
    )
    file_handler.setFormatter(formatter)
    file_handler.suffix = "%Y-%m-%d"

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    queue_handler = QueueHandler(log_queue)
    logger.addHandler(queue_handler)

    listener = QueueListener(log_queue, file_handler, console_handler)
    listener.start()

    return logger


logger = setup_logger()