from lib.langgraph.graph.state import State


async def retrieve_node(state: State) -> State:
    """
    문서 검색 노드 (RAG)

    지금:
    - 더미 데이터 반환

    나중:
    - Vector DB
    - BM25
    - Hybrid Search
    """

    # TODO: 실제 retriever로 교체
    dummy_docs = [
        "LangGraph는 상태 기반 워크플로우 프레임워크입니다.",
        "RAG는 검색 결과를 LLM 입력에 포함시키는 방식입니다.",
    ]

    return {
        **state,
        "retrieved_docs": dummy_docs,
    }
