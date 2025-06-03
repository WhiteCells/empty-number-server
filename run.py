# from app import app
from app.utils.logger import logger
from app.config import Config

if __name__ == "__main__":
    logger.warning("测试")
    import uvicorn
    uvicorn.run("app:app", host=Config.HOST, port=Config.PORT, reload=Config.RELOAD, workers=Config.WORKERS)