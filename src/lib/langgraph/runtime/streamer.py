import uuid
from typing import Any

import orjson
from anyio.streams.memory import MemoryObjectSendStream

from lib.langgraph.graph.workflow.base import StreamData
from lib.langgraph.graph.workflow.base import LangGraphWorkflow

from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser


def _to_json(data: StreamData) -> str:
    return orjson.dumps(data).decode()

async def stream_worker(
    *,
    workflow: LangGraphWorkflow,
    thread_id: str,
    messages: list[dict[str, Any]],
    send: MemoryObjectSendStream,
    message_parser: StrOutputParser
):
    thread_ended = False
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
                            msg = message_parser.invoke(chunk)
                            await send.send(
                                _to_json(
                                    {
                                        "id": event["run_id"],
                                        "type": "amc",
                                        "data": msg,
                                    }
                                )
                            )

                    case "on_chain_end":
                        if not thread_ended:
                            thread_ended = True
                            await send.send(
                                _to_json(
                                    {
                                        "id": str(uuid.uuid4()),
                                        "type": "thread_end",
                                        "data": {"thread_id": thread_id},
                                    }
                                )
                            )
                            break
        except Exception as e:
            await send.send(
                _to_json(
                    {
                        "id": str(uuid.uuid4()),
                        "type": "thread_error",
                        "data": {"error": str(e)},
                    }
                )
            )
