from typing import Annotated, NotRequired, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class State(TypedDict):
    """
    LangGraph State

    - 노드 간에 전달되는 실행 상태
    - Checkpointer 대상
    """

    # 대화 메시지 (필수)
    messages: Annotated[list[BaseMessage], add_messages]
    # ---- RAG 확장용 (지금은 사용 안 함) ----
    retrieved_docs: NotRequired[list[str]]
    need_retrieve: NotRequired[bool]
