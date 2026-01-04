from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRouter
from contextlib import asynccontextmanager

from src.infrastructure.config import confisettings
from src.user_interface.restapi.router.summary import summary_router
from src.user_interface.restapi.router.healthz import healthz_router


@asynccontextmanager
async def lifespan(_app: FastAPI):
    yield


app = FastAPI(
    lifespan=lifespan,
)

if confisettings.is_local:
    from starlette.middleware.cors import CORSMiddleware

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

root_router = APIRouter(prefix="/v1")
root_router.include_router(summary_router)
app.include_router(root_router)  # type: ignore
app.include_router(healthz_router)
