from typing import Awaitable, Callable
import time
import logging
from fastapi import (
    FastAPI,
    Request,
    Response,
    APIRouter,
    status,
)
from custom import CustomMidlleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

app = FastAPI()


def setup_middleware():
    # app.add_middleware(
    #     TrustedHostMiddleware,
    #     allowed_hosts=[
    #         "localhost",
    #     ],
    # )
    app.add_middleware(
        CustomMidlleware,
        router=app,
        ignore={
            dashboard,
        },
    )


hello_router = APIRouter(
    prefix="/hello",
)
logger = logging.getLogger("middleware_logger")
logging.basicConfig(level=logging.INFO)

requests = dict()


# @app.middleware("http")
# async def requests_count(
#     request: Request,
#     call_next: Callable[[Request], Awaitable[Response]],
# ) -> Response:
#     print(requests_count.__name__)
#     # print(f"{request.__getattribute__('nyx')=}")
#     response = await call_next(request)
#     if request.method not in requests.keys():
#         requests[request.method] = [
#             id(request),
#         ]
#     else:
#         requests.get(request.method).append(id(request))
#     return response


# @app.middleware("http")
# async def log_requests(
#     request: Request,
#     call_next: Callable[[Request], Awaitable[Response]],
# ) -> Response:
#     print(log_requests.__name__)  # BEFORE
#     start_time = time.time()
#     response = await call_next(request)  # CALL BUSINESS LOGIC
#     response: Response
#     process_time = (time.time() - start_time) * 1000  # AFTER
#     if response.status_code == status.HTTP_404_NOT_FOUND:
#         return Response("Bad idea", status_code=status.HTTP_402_PAYMENT_REQUIRED)
#     logger.info(
#         f"Запит: {request.method} {request.url} - Затрачений час: {process_time}ms"
#     )
#     logger.info(f"Відповідь: {response.status_code} ")

#     return response


@app.get("/")
async def read_root():
    return {"message": "Hello World"}


@hello_router.get("/dashboard")
async def dashboard():
    return requests


app.include_router(hello_router)
setup_middleware()
# app.middleware("http")(log_requests)
