from __future__ import annotations

from lib.langgraph.graph.workflow.base import LangGraphWorkflow
from lib.langgraph.graph.workflow.workflow import build_workflow
from lib.langgraph.llm.model import ModelID


class SingleAgentWorkflowFactory:
    """
    LangGraph Single-Agent Workflow Factory

    책임:
    - workflow(graph) 생성
    - store / checkpointer 주입
    - LangGraphWorkflow(Runtime wrapper) 반환

    """

    def __init__(
        self,
        *,
        model_id: ModelID = ModelID.OPENAI_GPT_41_MINI,
    ):
        self.model_id = model_id

    def build(
        self,
        *,
        user_id: str,
    ) -> LangGraphWorkflow:
        """
        LangGraphWorkflow 인스턴스 생성
        """

        graph = build_workflow()

        return LangGraphWorkflow(
            user_id=user_id,
            model_id=self.model_id,
            graph=graph,
        )
