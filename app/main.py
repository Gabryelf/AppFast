from fastapi import FastAPI
import uvicorn
from handlers import router


def get_app() -> FastAPI:
    application = FastAPI()
    application.include_router(router)
    return application


app = get_app()

if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)

