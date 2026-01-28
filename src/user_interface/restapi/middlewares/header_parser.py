from typing import TypedDict
from uuid import UUID

from starlette.datastructures import Headers
from starlette.types import ASGIApp, Receive, Scope, Send


class RequiredHeaders(TypedDict):
    request_id: UUID
    user_id: str
    client_ip: str


class HeaderParserMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    @staticmethod
    def _get_client_ip(scope: Scope):
        return scope.get("client", ("0.0.0.0", None))[0]

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        headers = Headers(scope=scope)

        state = scope.setdefault("state", {})
        state.update(
            RequiredHeaders(
                request_id=headers.get("x-request-id", "123123123"),
                user_id=headers.get("x-forwarded-user", "-1"),
                client_ip=headers.get("x-envoy-external-address", self._get_client_ip(scope)),
            )
        )
        await self.app(scope, receive, send)
