from lib.langgraph.graph.state import State


def decide_retrieve(state: State) -> bool:
    """
    RAG 검색 필요 여부 판단

    지금:
    - 항상 False (일반 챗봇)

    나중:
    - 질문 길이
    - 키워드
    - 이전 실패 여부 등
    """

    last = state["messages"][-1].content
    if not isinstance(last, str):
        return False

    # 예시 룰 (나중에 교체)
    keywords = ["문서", "자료", "근거", "출처"]
    return any(k in last for k in keywords)
