from typing import Annotated
from fastapi import Depends, HTTPException, Request


from lib.langgraph.graph.workflow.base import LangGraphWorkflow


async def get_user_id(request: Request) -> str:
    user_id = getattr(request.state, "user_id", None)
    if not user_id:
        raise HTTPException(403)

    return user_id


UserIDDeps = Annotated[str, Depends(get_user_id)]


async def get_langgraph_agent_workflow() -> LangGraphWorkflow:
    return LangGraphWorkflow()


LangGraphWorkflowDeps = Annotated[LangGraphWorkflow, Depends(get_langgraph_agent_workflow)]
