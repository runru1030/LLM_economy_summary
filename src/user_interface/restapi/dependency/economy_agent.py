from typing import Annotated

from fastapi import Depends, HTTPException, Request
from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.store.memory import InMemoryStore
from langgraph.store.postgres.aio import AsyncPostgresStore

from lib.langgraph.graph.workflow.base import LangGraphWorkflow
from lib.langgraph.graph.workflow.factory import SingleAgentWorkflowFactory


async def get_user_id(request: Request) -> str:
    user_id = getattr(request.state, "user_id", None)
    if not user_id:
        raise HTTPException(403)

    return user_id


UserIDDeps = Annotated[str, Depends(get_user_id)]


async def get_langgraph_agent_workflow() -> LangGraphWorkflow:
    return LangGraphWorkflow()


LangGraphWorkflowDeps = Annotated[LangGraphWorkflow, Depends(get_langgraph_agent_workflow)]


async def get_saver(request: Request) -> MemorySaver | AsyncPostgresSaver:
    return request.app.saver


SaverDeps = Annotated[MemorySaver | AsyncPostgresSaver, Depends(get_saver)]


async def get_store(request: Request) -> InMemoryStore | AsyncPostgresStore:
    return request.app.store


StoreDeps = Annotated[InMemoryStore | AsyncPostgresStore, Depends(get_store)]


async def get_single_agent_workflow(
    user_id: UserIDDeps,
    saver: SaverDeps,
    store: StoreDeps,
) -> LangGraphWorkflow:
    return SingleAgentWorkflowFactory().build(
        user_id=user_id,
        checkpointer=saver,
        store=store,
    )


SingleAgentWorkflowDeps = Annotated[LangGraphWorkflow, Depends(get_single_agent_workflow)]
