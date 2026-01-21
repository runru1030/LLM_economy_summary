import os
import typing
from collections.abc import Callable, Sequence
from enum import StrEnum
from functools import cache
from typing import Any

from dotenv import load_dotenv
from langchain_core.language_models import (
    BaseChatModel,
    FakeListChatModel,
    LanguageModelInput,
)
from langchain_core.messages import BaseMessage
from langchain_core.runnables import Runnable
from langchain_core.tools import BaseTool
from langchain_openai import ChatOpenAI

__all__ = ("ModelID", "get_model")

load_dotenv()


class CustomFakeListChatModel(FakeListChatModel):
    def bind_tools(
        self,
        tools: Sequence[
            typing.Dict[str, Any] | type | Callable | BaseTool  # noqa: UP006
        ],
        **kwargs: Any,
    ) -> Runnable[LanguageModelInput, BaseMessage]:
        return self


class ModelID(StrEnum):
    OPENAI_GPT_41_MINI = "gpt-4.1-mini"
    FAKE = "fake"


@cache
def get_model(model_id: ModelID, temperature: float = 0.5) -> BaseChatModel:
    match model_id:
        case ModelID.OPENAI_GPT_41_MINI:
            return ChatOpenAI(
                model_name=model_id,
                openai_api_key=os.getenv("OPENAI_API_KEY"),
                temperature=temperature,
            )
        case ModelID.FAKE:
            return CustomFakeListChatModel(responses=["Fake response."])
        case _:
            raise NotImplementedError(f"Model {model_id} is not implemented.")
