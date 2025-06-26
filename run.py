from app.config import Config


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", 
                host=Config.SERVER_HOST, 
                port=Config.SERVER_PORT, 
                # reload=Config.DEBUG, 
                workers=Config.WORKERS)