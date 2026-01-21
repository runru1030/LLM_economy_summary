from __future__ import annotations

from langgraph.graph import StateGraph, END
from langgraph.graph.state import CompiledStateGraph

from lib.langgraph.graph.state import State
from lib.langgraph.graph.nodes.chat import chat_node
from lib.langgraph.graph.nodes.decide import decide_retrieve
from lib.langgraph.graph.nodes.retrieve import retrieve_node
from lib.langgraph.llm.model import ModelID

def build_workflow() -> CompiledStateGraph:
    """
    LangGraph Workflow Builder

    책임:
    - StateGraph 정의
    - 노드 연결
    - 조건부 분기 정의
    - compile 후 CompiledStateGraph 반환
    """

    graph = StateGraph(State)

    graph.add_node("chat", chat_node)
    graph.add_node("retrieve", retrieve_node)

    graph.set_entry_point("chat")

    graph.add_conditional_edges(
        "chat",
        decide_retrieve,  # bool 반환
        {
            True: "retrieve",
            False: END,
        },
    )

    graph.add_edge("retrieve", "chat")

    return graph.compile(
        name="single-agent-workflow",
    )
