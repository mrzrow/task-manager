from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from .api import router_v1
from .models.base import Base
from .db.session import engine


@asynccontextmanager
async def lifespan(_app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    try:
        yield
    finally:
        await engine.dispose()



app = FastAPI(title='Task Manager API', prefix="/api", lifespan=lifespan)
app.include_router(router_v1)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)

