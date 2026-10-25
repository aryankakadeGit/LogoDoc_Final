"""
Caps the size of JSON request bodies (recommendation endpoints). A real analysis is ~20 KB,
so 256 KB is generous. The image upload route reads its own body with its own limit.
"""

from starlette.responses import JSONResponse
from starlette.types import ASGIApp, Message, Receive, Scope, Send

MAX_JSON_BYTES = 256 * 1024
_SKIP_PATHS = {"/api/logo/analyze"}


class JsonBodyLimit:
    """ASGI middleware: reads the body up to the limit, answers 413 if it is bigger,
    otherwise hands the same body on to the app unchanged."""

    def __init__(self, app: ASGIApp, max_bytes: int = MAX_JSON_BYTES) -> None:
        self.app = app
        self.max_bytes = max_bytes

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http" or scope["method"] != "POST" or scope["path"] in _SKIP_PATHS:
            await self.app(scope, receive, send)
            return

        body = bytearray()
        more_body = True
        while more_body:
            message = await receive()
            if message["type"] != "http.request":  # client disconnected
                return
            body += message.get("body", b"")
            more_body = message.get("more_body", False)
            if len(body) > self.max_bytes:
                response = JSONResponse(
                    status_code=413,
                    content={"error": {"code": "REQUEST_TOO_LARGE", "message": "The request is too large."}},
                )
                await response(scope, receive, send)
                return

        replayed = False

        async def replay() -> Message:
            nonlocal replayed
            if not replayed:
                replayed = True
                return {"type": "http.request", "body": bytes(body), "more_body": False}
            return await receive()

        await self.app(scope, replay, send)