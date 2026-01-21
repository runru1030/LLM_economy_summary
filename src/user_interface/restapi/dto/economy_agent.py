import uuid
from typing import Annotated, Literal

from pydantic import BaseModel, Field, StringConstraints


class TextMessage(BaseModel):
    type: Literal["text"] = "text"
    text: Annotated[
        str,
        StringConstraints(strip_whitespace=True, min_length=1, max_length=10000),
        Field(description="텍스트 메시지입니다."),
    ]


class ThreadRequest(BaseModel):
    thread_id: uuid.UUID | None = Field(
        None,
        description="메시지를 전송할 채팅방 ID입니다. 없으면 새로운 채팅방을 생성합니다.",
    )
    messages: list[Annotated[TextMessage, Field(discriminator="type")]] = Field(
        description="전송할 메시지입니다.", min_length=1, max_length=10
    )


class ReplayAnswerRequest(BaseModel):
    message_id: str | None = None


class ThreadResponse(BaseModel):
    id: str
    type: Literal[
        "hm",
        "am",
        "amc",
        "tm",
        "thread_start",
        "thread_error",
        "tool_start",
    ]
    data: str | list | dict

