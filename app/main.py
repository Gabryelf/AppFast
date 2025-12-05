from fastapi import FastAPI
import uvicorn
import os
from fastapi.staticfiles import StaticFiles
from handlers import router
from config import STATIC_DIR


def get_app() -> FastAPI:
    application = FastAPI()
    application.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
    application.include_router(router)
    return application


app = get_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    uvicorn.run(app, host='localhost', port=port)
