from fastapi import FastAPI
import uvicorn
import os
import sys
from fastapi.staticfiles import StaticFiles

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.handlers import router
from app.config import STATIC_DIR
from app.models import create_tables


def get_app() -> FastAPI:
    application = FastAPI(title="Item Gallery API")
    create_tables()
    application.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
    application.include_router(router)
    return application


app = get_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    uvicorn.run("app.main:app", host='0.0.0.0', port=port)
    