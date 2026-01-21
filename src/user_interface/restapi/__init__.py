from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRouter
from fastapi.middleware import Middleware

from infrastructure.config import confisettings
from user_interface.restapi.router.healthz import healthz_router
from user_interface.restapi.router.summary import summary_router
from user_interface.restapi.router.economy_agent import economy_agent_router
from user_interface.restapi.middlewares.header_parser import HeaderParserMiddleware
from user_interface.restapi.middlewares.logger import LoggingMiddleware


@asynccontextmanager
async def lifespan(_app: FastAPI):
    yield


app = FastAPI(
    lifespan=lifespan,
    middleware=[
        Middleware(HeaderParserMiddleware),
        Middleware(LoggingMiddleware),
    ],
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
root_router.include_router(economy_agent_router)
app.include_router(root_router)  # type: ignore
app.include_router(healthz_router)
