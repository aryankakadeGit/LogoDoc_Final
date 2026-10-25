"""
Logging setup. Never logs image bytes, API keys or full AI payloads.
"""
"""
One logging setup for the whole app. Called once from main.py at startup.

Modules log with the standard library:
    logger = logging.getLogger(__name__)

Rule: never log image bytes, API keys or full AI payloads.
"""

import logging

_FORMAT = "%(asctime)s %(levelname)-8s %(name)s  %(message)s"


def setup_logging(level: str = "INFO") -> None:
    logging.basicConfig(level=level, format=_FORMAT, force=True)
    # HTTP client used by the AI SDK logs every request at INFO; keep only problems.
    logging.getLogger("httpx").setLevel(logging.WARNING)