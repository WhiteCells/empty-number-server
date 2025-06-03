from asyncio import Handle


class Config:
    # 应用配置
    DEBUG: bool = True
    # 是否自动重载
    RELOAD: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 1  # 工作进程数，根据需要调整

    # MySQL 配置
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: str = "3306"
    MYSQL_USER: str = "root"
    MYSQL_PASS: str = "admin1"
    MYSQL_DB: str = "test"

    # Redis 配置
    REDIS_HOST: str = "localhost"
    REDIS_PORT: str = "6379"
    REDIS_DB: int = 0
    REDIS_PASS: str = ""

    # Logger 配置
    LOG_LEVEL: str = "DEBUG"
    LOG_DIR: str = "logs"
    LOG_BACKUP_COUNT: int = 7

    # JWT 配置
    JWT_SECRET_KEY: str = "your-secret-key"  # 生产环境中应从安全位置获取
    JWT_ALGORITHM: str = "HS256"  # 加密算法
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # 访问令牌的过期时间（分钟）
    JWT_REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 刷新令牌的过期时间（分钟）
    JWT_COOKIE_NAME: str = "refresh_token"  # 刷新令牌的 Cookie 名称
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
    def REDIS_URL() -> str:
        auth = f":{Config.REDIS_PASS}@" if Config.REDIS_PASS else ""
        return f"redis://{auth}{Config.REDIS_HOST}:{Config.REDIS_PORT}/{Config.REDIS_DB}"
