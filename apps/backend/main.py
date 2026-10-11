from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from infrastructure.redis import redis_manager


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    await redis_manager.connect()
    yield
    await redis_manager.close()


app = FastAPI(lifespan=lifespan)
