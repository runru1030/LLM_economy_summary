import logging
from typing import Any, Literal

from langchain_core.messages import BaseMessage, RemoveMessage
from langfuse.langchain import CallbackHandler
from langgraph.graph.state import CompiledStateGraph
from typing_extensions import TypedDict
from lib.langgraph.llm.model import ModelID
from langchain_core.runnables import RunnableConfig

logger = logging.getLogger(__name__)
langfuse_handler = CallbackHandler()


# ------------------------------------------------------------------
# Public DTOs (API / Runtime 공용)
# ------------------------------------------------------------------
class TextMessage(TypedDict):
    type: Literal["text"]
    text: str


class FileMessage(TypedDict):
    type: Literal["image", "document"]
    filename: str


class StreamData(TypedDict):
    id: str
    type: str
    data: Any


ThreadID = str


# ------------------------------------------------------------------
# LangGraph Runtime Wrapper
# ------------------------------------------------------------------
class LangGraphWorkflow:
    """
    LangGraph Runtime Wrapper

    책임:
    - thread_id → LangGraph thread key 변환
    - LangGraph state 조회 / 수정
    - 메시지 삭제 / 롤백
    - thread metadata 접근 (graph.store)
    """

    def __init__(self, user_id: str, model_id: ModelID , graph: CompiledStateGraph):
        self.user_id = user_id
        self.model_id = model_id
        self.graph = graph
        self.trace_handler = langfuse_handler

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _thread_key(self, thread_id: ThreadID) -> str:
        """LangGraph에서 사용할 실제 thread key"""
        return f"{self.user_id}-{thread_id}"

    def _config(self, thread_id: ThreadID) -> dict:
        """LangGraph RunnableConfig용 최소 config"""
        return {"configurable": {"thread_id": self._thread_key(thread_id),  "model_id": self.model_id,}}

    # ------------------------------------------------------------------
    # Message APIs
    # ------------------------------------------------------------------
    async def get_messages(self, thread_id: ThreadID) -> list[dict[str, Any]]:
        """현재 thread의 메시지 목록 조회"""
        state = await self.graph.aget_state(self._config(thread_id))
        messages: list[BaseMessage] = state.values.get("messages", [])

        result: list[dict[str, Any]] = []
        for msg in messages:
            if not msg.content:
                continue

            if msg.type == "ai":
                result.append({"id": msg.id, "role": "assistant", "content": msg.content})
            elif msg.type == "human":
                result.append({"id": msg.id, "role": "user", "content": msg.content})
            elif msg.type == "tool":
                result.append(
                    {
                        "id": msg.id,
                        "role": "tool",
                        "content": msg.content,
                        "artifact": msg.artifact,
                    }
                )

        return result

    async def delete_message(self, thread_id: ThreadID, message_id: str) -> None:
        """특정 메시지 삭제"""
        await self.graph.aupdate_state(
            self._config(thread_id),
            {"messages": [RemoveMessage(id=message_id)]},
        )

    async def delete_after(self, thread_id: ThreadID, message_id: str) -> None:
        """특정 메시지 이후 모든 메시지 삭제"""
        state = await self.graph.aget_state(self._config(thread_id))
        messages: list[BaseMessage] = state.values.get("messages", [])

        delete = False
        for msg in messages:
            if msg.id is None:
                continue

            if msg.id == message_id:
                delete = True

            if delete:
                try:
                    await self.delete_message(thread_id, msg.id)
                except Exception:
                    logger.exception(
                        "failed_to_delete_message",
                        extra={
                            "thread_id": thread_id,
                            "message_id": msg.id,
                        },
                    )

    async def rollback_last_message(self, thread_id: ThreadID) -> None:
        """
        마지막 메시지 이전 상태로 롤백
        (LangGraph state history 기반)
        """
        last_snapshot = None

        async for snapshot in self.graph.aget_state_history(self._config(thread_id)):
            if snapshot.next == ():
                last_snapshot = snapshot
                break

        if last_snapshot is None:
            logger.debug(
                "no_state_to_rollback",
                extra={"thread_id": thread_id},
            )
            return

        await self.graph.aupdate_state(
            last_snapshot.config,
            last_snapshot.values,
        )

    def get_runnable_config(self, thread_id: str) -> RunnableConfig:
        return RunnableConfig(
            configurable={
                "thread_id": self._thread_key(thread_id),
                "model_id": self.model_id,
            },
            callbacks=[self.trace_handler],
        )
