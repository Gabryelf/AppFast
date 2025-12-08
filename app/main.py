from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.routers import api_router, pages_router
from app.config import settings
from app.database import init_database

app = FastAPI(
    title="Item Gallery API",
    description="API для управления галереей предметов",
    version="1.0.0"
)

try:
    init_db()
except Exception as e:
    print(f"Warning: {e}")

app.mount("/static", StaticFiles(directory=settings.STATIC_DIR), name="static")

app.include_router(pages_router)
app.include_router(api_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000)),
        reload=settings.DEBUG
    )