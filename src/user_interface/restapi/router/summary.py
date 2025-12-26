from fastapi.routing import APIRouter

summary_router = APIRouter(
    prefix="/summary",
    tags=["summary"],
)


@summary_router.get("/")
async def get_summary():
    return {"message": "Hello, World!"}
