from uuid import uuid4

from anyio import create_memory_object_stream
from langchain_core.output_parsers import StrOutputParser
from sse_starlette import EventSourceResponse

from lib.langgraph.graph.workflow.base import LangGraphWorkflow
from lib.langgraph.graph.workflow.factory import SingleAgentWorkflowFactory
from lib.langgraph.runtime.streamer import stream_worker
from user_interface.restapi.dto.economy_agent import (
    ReplayAnswerRequest,
    TextMessage,
    ThreadRequest,
)


class AgentManager:
    def __init__(
        self,
        *,
        workflow: LangGraphWorkflow,
    ):
        self.workflow = workflow
        self._message_parser = StrOutputParser()

    # ------------------------------------------------------------
    # New conversation
    # ------------------------------------------------------------
    async def generate_answer(
        self,
        *,
        body: ThreadRequest,
    ):
        thread_id = str(body.thread_id or uuid4())

        # text 없으면 자동 추가
        if all(m.type != "text" for m in body.messages):
            body.messages.append(TextMessage(text="Briefly summarize the uploaded files."))

        body.messages.sort(key=lambda x: x.type == "text")

        send, recv = create_memory_object_stream(float("inf"))

        async def _runner():
            # try:
            await stream_worker(
                workflow=self.workflow,
                thread_id=thread_id,
                messages=[m.model_dump() for m in body.messages],
                send=send,
                message_parser=self._message_parser,
            )
            # finally:
            # self.locks.release(thread_id)

        return EventSourceResponse(
            recv,
            data_sender_callable=_runner,
            send_timeout=120,
        )

    # ------------------------------------------------------------
    # Replay
    # ------------------------------------------------------------
    async def replay_answer(
        self,
        *,
        thread_id: str,
        body: ReplayAnswerRequest,
    ):
        try:
            messages = await self.workflow.get_messages(thread_id)
            if not messages:
                raise ValueError("MessageNotFound")

            target_id = body.message_id or messages[-1]["id"]
            await self.workflow.delete_after(thread_id, target_id)

            last_text = messages[-1]["content"][-1]["text"]

            send, recv = create_memory_object_stream(float("inf"))

            async def _runner():
                await stream_worker(
                    workflow=self.workflow,
                    thread_id=thread_id,
                    messages=[{"type": "text", "text": last_text}],
                    send=send,
                    replay=True,
                    message_parser=self._message_parser,
                )

            return EventSourceResponse(
                recv,
                data_sender_callable=_runner,
                send_timeout=120,
            )

        except Exception:
            raise

    async def get_history(self, thread_id: str, user_id: str):
        # TODO user_id 활용
        messages = await self.workflow.get_messages(str(thread_id))

        result = []
        for message in messages:
            data = message.get("data", [{}])
            if isinstance(data, list) and len(data) > 0:
                if data[0].get("text") == "Briefly summarize the core contents of the files.":
                    continue

            result.append(message)

        return {
            "thread_id": str(thread_id),
            "messages": result,
        }
