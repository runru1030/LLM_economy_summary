import uuid
from typing import Any

import orjson
from anyio.streams.memory import MemoryObjectSendStream

from lib.langgraph.graph.workflow.base import StreamData
from lib.langgraph.graph.workflow.base import LangGraphWorkflow

from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig


def _to_json(data: StreamData) -> str:
    return orjson.dumps(data).decode()

async def stream_worker(
    *,
    workflow: LangGraphWorkflow,
    thread_id: str,
    messages: list[dict[str, Any]],
    send: MemoryObjectSendStream,
):
    await send.send(
        _to_json(
            {
                "id": str(uuid.uuid4()),
                "type": "thread_start",
                "data": {"thread_id": thread_id},
            }
        )
    )
    async with send:
        try:
            async for event in workflow.graph.astream_events(
                input={"messages": [HumanMessage([m]) for m in messages]},
                config=workflow.get_runnable_config(thread_id),
            ):
                match event["event"]:
                    case "on_chat_model_stream":
                        chunk = event["data"].get("chunk")
                        if chunk and chunk.content:
                            await send.send(
                                _to_json(
                                    {
                                        "id": event["run_id"],
                                        "type": "assistant_chunk",
                                        "data": chunk.content,
                                    }
                                )
                            )

                    case "on_chain_end":
                        await send.send(
                            _to_json(
                                {
                                    "id": str(uuid.uuid4()),
                                    "type": "conversation_end",
                                    "data": {"thread_id": thread_id},
                                }
                            )
                        )
        except Exception as e:
            await send.send(
                _to_json(
                    {
                        "id": str(uuid.uuid4()),
                        "type": "conversation_error",
                        "data": {"error": str(e)},
                    }
                )
            )
