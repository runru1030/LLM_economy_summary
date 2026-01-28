import time
from typing import Any, NotRequired, TypedDict

from fastapi.responses import ORJSONResponse
from loguru import _logger, logger
from starlette.datastructures import Headers
from starlette.types import ASGIApp, Message, Receive, Scope, Send
from uvicorn.protocols.utils import ClientDisconnected


class LoggingData(TypedDict):
    method: str | None
    url: str
    user_id: str
    email: str
    request_id: str
    remote_address: str
    user_agent: str
    status: NotRequired[int]
    latency: NotRequired[float]
    thread_id: NotRequired[str]
    error_code: NotRequired[int]
    error_message: NotRequired[str]


class LoggingMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    @staticmethod
    def _extract_logging_data(scope: Scope):
        state = scope.setdefault("state", {})
        query_string = scope.get("query_string", b"").decode()
        path = scope.get("path", "")
        url = path + (f"?{query_string}" if query_string else "")
        header = Headers(scope=scope)

        return LoggingData(
            user_id=state.get("user_id", "-1"),
            request_id=str(state.get("request_id")),
            remote_address=state.get("client_ip", "0.0.0.0"),
            user_agent=header.get("user-agent", "unknown"),
            method=scope.get("method"),
            url=url,
        )

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        start_time = time.time()
        res_message: dict[str, Any] = {}

        async def wrapped_send(message: Message) -> None:
            if message["type"] == "http.response.start":
                res_message.update(message)
            await send(message)

        logging_data = self._extract_logging_data(scope)

        with logger.contextualize(**logging_data):
            try:
                await self.app(scope, receive, wrapped_send)
            except ClientDisconnected:
                pass
            except Exception as e:
                status_code = getattr(e, "status_code", 500)
                error_code = getattr(e, "error_code", -1)
                error_message = getattr(e, "error_message", "Internal Server Error")
                if status_code == 500:
                    logger.exception(e)
                else:
                    res_message["status"] = status_code
                    _logger.context.get().update(
                        {
                            "status": status_code,
                            "error_code": error_code,
                            "error_message": error_message,
                        }
                    )
                error_response = ORJSONResponse(
                    status_code=status_code,
                    content={"error": {"code": error_code, "message": error_message}},
                )
                await error_response(scope, receive, wrapped_send)
            finally:
                logger.info(
                    "request",
                    latency=time.time() - start_time,
                    status=res_message.get("status", 500),
                )
