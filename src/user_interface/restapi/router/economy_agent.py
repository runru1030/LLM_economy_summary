import uuid

from fastapi import APIRouter

from application.usecase.agent_manager import AgentManager
from user_interface.restapi.dependency.economy_agent import SingleAgentWorkflowDeps, UserIDDeps
from user_interface.restapi.dto.economy_agent import (
    ReplayAnswerRequest,
    ThreadHistoryResponse,
    ThreadRequest,
    ThreadResponse,
)

ALLOW_MIME = {
    "image/png",
    "image/jpeg",
    "image/gif",
    "image/webp",
    "application/pdf",
    "text/csv",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.ms-excel",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "text/html",
    "text/plain",
    "text/xml",
    "text/markdown",
    "chemical/x-mdl-sdfile",
    "application/vnd.chemdraw+xml",
    "text/tab-separated-values",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation",
}

economy_agent_router = APIRouter(prefix="/economy-agent", tags=["economy agent"])


@economy_agent_router.post(
    "/chat",
    description="실시간 대화",
)
async def chat(
    workflow: SingleAgentWorkflowDeps,
    body: ThreadRequest,
):
    agent_manager = AgentManager(workflow=workflow)
    return await agent_manager.generate_answer(
        body=body,
    )


@economy_agent_router.post(
    "/chat/{thread_id}/replay",
    description="실시간 대화",
    response_model=ThreadResponse,
)
async def replay_thread(
    thread_id: str,
    user_id: UserIDDeps,
    workflow: SingleAgentWorkflowDeps,
    body: ReplayAnswerRequest,
):
    agent_manager = AgentManager(workflow=workflow)
    return await agent_manager.replay_answer(
        user_id=user_id,
        thread_id=str(thread_id),
        body=body,
    )


@economy_agent_router.get(
    "/thread/{thread_id}",
    status_code=200,
    response_model=ThreadHistoryResponse,
)
async def thread_history(
    user_id: UserIDDeps,
    thread_id: uuid.UUID,
    workflow: SingleAgentWorkflowDeps,
):
    agent_manager = AgentManager(workflow=workflow)
    return await agent_manager.get_history(thread_id=thread_id, user_id=user_id)
