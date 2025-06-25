import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DEBUG: bool = True
    WORKERS: int = 3

    # Server 配置
    SERVER_HOST: str = os.getenv("SERVER_HOST")
    SERVER_PORT: int = int(os.getenv("SERVER_PORT"))

    # MySQL 配置
    MYSQL_HOST: str = os.getenv("MYSQL_HOST")
    MYSQL_PORT: str = os.getenv("MYSQL_PORT")
    MYSQL_USER: str = os.getenv("MYSQL_USER")
    MYSQL_PASS: str = os.getenv("MYSQL_PASS")
    MYSQL_DB: str = os.getenv("MYSQL_DB")
    MYSQL_POOL_SIZE: int = 10       # 最大连接数
    MYSQL_POOL_TEMP: int = 20       # 最大溢出连接
    MYSQL_POOL_RECYCLE: int = 1800  # 连接最大生命周期（秒） 

    # Redis 配置
    REDIS_HOST: str = os.getenv("REDIS_HOST")
    REDIS_PORT: str = os.getenv("REDIS_PORT")
    REDIS_DB: int = int(os.getenv("REDIS_DB"))
    REDIS_PASS: str = os.getenv("REDIS_PASS")
    REDIS_MAX_CONN: int = 50

    # WAV UPLOAD 配置
    UPLOADS_DIR: str = "uploads"

    # Logger 配置
    LOG_LEVEL: str = "DEBUG"
    LOG_DIR: str = "logs"
    LOG_BACKUP_COUNT: int = 7
    LOG_FORMAT: str = "[%(asctime)s] [%(levelname)s] [Thread ID: %(thread)d] [%(filename)s:%(lineno)d] %(message)s"

    @staticmethod
    def DATABASE_URL() -> str:
        return (
            f"mysql+aiomysql://{Config.MYSQL_USER}:{Config.MYSQL_PASS}"
            f"@{Config.MYSQL_HOST}:{Config.MYSQL_PORT}/{Config.MYSQL_DB}"
        )
    
    @staticmethod
    def SYNC_DATABASE_URL() -> str:
        return (
            f"mysql+pymysql://{Config.MYSQL_USER}:{Config.MYSQL_PASS}"
            f"@{Config.MYSQL_HOST}:{Config.MYSQL_PORT}/{Config.MYSQL_DB}"
        )

    @staticmethod
    def REDIS_URL() -> str:
        auth = f":{Config.REDIS_PASS}@" if Config.REDIS_PASS else ""
        return f"redis://{auth}{Config.REDIS_HOST}:{Config.REDIS_PORT}/{Config.REDIS_DB}"
