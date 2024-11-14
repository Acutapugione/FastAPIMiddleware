from typing import Awaitable, Callable
from fastapi import Request, Response, status, FastAPI
from starlette.middleware.base import BaseHTTPMiddleware


class CustomMidlleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: BaseHTTPMiddleware,
        router: FastAPI,
        ignore: set[Callable[[Request], Awaitable[Response]]] = set(),
    ):
        super().__init__(app)
        self.ignore = [router.url_path_for(x.__name__) for x in ignore]

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        # BEFORE
        # print(f"{self.ignore=}{request.scope.get("path")=}")
        if request.scope.get("path") in self.ignore:
            return Response("Not operational", status_code=status.HTTP_410_GONE)
        response = await call_next(request)
        # AFTER
        return response
