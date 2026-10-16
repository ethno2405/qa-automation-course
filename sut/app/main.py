"""Course shop: the practice application (system under test) of the QA automation course."""

import asyncio
import os
import random
import time
import uuid
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, Response
from fastapi.staticfiles import StaticFiles

from app import api, ui
from app.logs import log_error, log_request, request_id
from app.rules import RuleError

VERSION = "1.0.0"
LATENCY_MS = int(os.environ.get("SUT_LATENCY_MS", "0"))

app = FastAPI(
    title="Course Shop API",
    version=VERSION,
    description="The practice application of the QA automation course. See REQUIREMENTS.md.",
)
app.state.version = VERSION


@app.middleware("http")
async def request_log(request: Request, call_next):  # type: ignore[no-untyped-def]
    rid = request.headers.get("X-Request-ID") or uuid.uuid4().hex[:12]
    token = request_id.set(rid)
    start = time.perf_counter()
    try:
        if LATENCY_MS > 0 and request.url.path.startswith("/api/") and request.url.path != "/api/health":
            await asyncio.sleep(random.uniform(0, LATENCY_MS) / 1000)
        try:
            response: Response = await call_next(request)
        except Exception as error:  # noqa: BLE001 - every unexpected error becomes a logged 500 response
            log_error("unhandled_error", error)
            response = JSONResponse({"error": "Internal server error."}, status_code=500)
        response.headers["X-Request-ID"] = rid
        log_request(request.method, request.url.path, response.status_code, (time.perf_counter() - start) * 1000)
        return response
    finally:
        request_id.reset(token)


@app.exception_handler(RuleError)
async def rule_error_handler(request: Request, error: RuleError) -> JSONResponse:
    body: dict[str, object] = {"error": error.message}
    if error.details:
        body["details"] = error.details
    return JSONResponse(body, status_code=error.status)


@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, error: RequestValidationError) -> JSONResponse:
    details = [
        {"field": ".".join(str(part) for part in item["loc"] if part != "body"), "message": item["msg"]}
        for item in error.errors()
    ]
    return JSONResponse({"error": "The request is not valid.", "details": details}, status_code=422)


app.include_router(api.router)
app.include_router(ui.router)
app.mount("/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static")
