from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
import sys


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.routers import api_router, pages_router
from app.config import settings
from app.database import create_tables

app = FastAPI(
    title="Item Gallery API",
    description="API для управления галереей предметов",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


@app.on_event("startup")
async def startup_event():
    if os.path.exists(settings.STATIC_DIR):
        static_files = os.listdir(settings.STATIC_DIR)
        print(f"Found {len(static_files)} static files")
    else:
        print("Static directory not found!")
    create_tables()

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
    