from __future__ import annotations

import json
from pathlib import Path

import loguru
from loguru import logger


def serialise(record: loguru.Record) -> str:
    """Serialise log record.

    Args:
        record: Log record.

    Returns:
        Serialised log record.
    """
    try:
        log_message = json.loads(record["message"])
    except json.JSONDecodeError:
        log_message = record["message"]

    log_entry = {
        "timestamp": record["time"].isoformat(),
        "level": record["level"].name,
        "message": log_message,
        "file": record["file"].name,
        "line": record["line"],
        "function": record["function"],
    }

    return json.dumps(log_entry)


def sink(message: loguru.Message) -> None:
    """Log sink.

    Args:
        message: Log message.
    """
    serialised = serialise(message.record)
    print(serialised)


def formatter(record: loguru.Record) -> str:
    """Record template for log file.

    Args:
        record: Log record.

    Returns:
        Log record template.
    """
    record["extra"]["serialised"] = serialise(record)
    return "{extra[serialised]}\n"


def load_logger(log_file: Path | None = None) -> None:
    logger.remove()
    if log_file:
        logger.add(str(log_file), format=formatter)
    else:
        logger.add(sink)
