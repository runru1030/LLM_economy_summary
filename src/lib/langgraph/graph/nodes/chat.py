from langchain_core.runnables import RunnableConfig

from lib.langgraph.graph.state import State
from lib.langgraph.llm.model import get_model


async def chat_node(
    state: State,
    config: RunnableConfig,
) -> State:
    """
    기본 LLM 응답 노드

    입력:
    - state.messages

    출력:
    - state.messages + AIMessage
    """

    llm = get_model(config["configurable"]["model_id"])

    response = await llm.ainvoke(state["messages"])

    if isinstance(response.content, str):
        response.content = [{"type": "text", "text": response.content}]

    return {
        "messages": [response],
    }
