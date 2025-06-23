import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DEBUG: bool = True
    WORKERS: int = 3

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

    # Logger 配置
    LOG_LEVEL: str = "DEBUG"
    LOG_DIR: str = "logs"
    LOG_BACKUP_COUNT: int = 7
    """
    %(name)s            Name of the logger (logging channel)
    %(levelno)s         Numeric logging level for the message (DEBUG, INFO,
                        WARNING, ERROR, CRITICAL)
    %(levelname)s       Text logging level for the message ("DEBUG", "INFO",
                        "WARNING", "ERROR", "CRITICAL")
    %(pathname)s        Full pathname of the source file where the logging
                        call was issued (if available)
    %(filename)s        Filename portion of pathname
    %(module)s          Module (name portion of filename)
    %(lineno)d          Source line number where the logging call was issued
                        (if available)
    %(funcName)s        Function name
    %(created)f         Time when the LogRecord was created (time.time()
                        return value)
    %(asctime)s         Textual time when the LogRecord was created
    %(msecs)d           Millisecond portion of the creation time
    %(relativeCreated)d Time in milliseconds when the LogRecord was created,
                        relative to the time the logging module was loaded
                        (typically at application startup time)
    %(thread)d          Thread ID (if available)
    %(threadName)s      Thread name (if available)
    %(process)d         Process ID (if available)
    %(message)s         The result of record.getMessage(), computed just as
                        the record is emitted
    """
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
