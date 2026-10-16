"""JSON log lines on the standard output (R7.3, R7.4)."""

import json
import sys
from contextvars import ContextVar
from datetime import UTC, datetime
from typing import Any

request_id: ContextVar[str] = ContextVar("request_id", default="-")


def _write(record: dict[str, Any]) -> None:
    record = {"ts": datetime.now(UTC).isoformat(timespec="milliseconds"), "request_id": request_id.get(), **record}
    sys.stdout.write(json.dumps(record) + "\n")
    sys.stdout.flush()


def log_request(method: str, path: str, status: int, duration_ms: float) -> None:
    level = "ERROR" if status >= 500 else "WARN" if status >= 400 else "INFO"
    _write({"level": level, "event": "http_request", "method": method, "path": path, "status": status, "duration_ms": round(duration_ms, 1)})


def log_event(event: str, **fields: Any) -> None:
    _write({"level": "INFO", "event": event, **fields})


def log_error(event: str, error: BaseException) -> None:
    _write({"level": "ERROR", "event": event, "error": type(error).__name__, "message": str(error)})
