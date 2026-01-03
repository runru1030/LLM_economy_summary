from fastapi import APIRouter

healthz_router = APIRouter(prefix="/healthz", include_in_schema=False)


@healthz_router.get("")
async def healthz():
    return {"status": "ok"}
