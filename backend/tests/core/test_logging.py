import logging

import pytest

from app.core.logging import setup_logging


@pytest.fixture(autouse=True)
def restore_logging():
    root = logging.getLogger()
    handlers, level = root.handlers[:], root.level
    yield
    root.handlers, root.level = handlers, level


def test_level_is_applied():
    setup_logging("WARNING")
    assert logging.getLogger().level == logging.WARNING


def test_format_has_time_level_module_and_message(capsys):
    setup_logging("INFO")
    logging.getLogger("app.modules.ai").info("Sending image to AI")
    line = capsys.readouterr().err.strip()
    assert line.endswith("INFO     app.modules.ai  Sending image to AI")
    assert line[:4].isdigit()  # starts with the date


def test_lower_levels_are_hidden(capsys):
    setup_logging("WARNING")
    logging.getLogger("x").info("hidden")
    logging.getLogger("x").warning("shown")
    err = capsys.readouterr().err
    assert "hidden" not in err and "shown" in err


def test_httpx_request_logs_are_quiet():
    setup_logging("DEBUG")
    assert logging.getLogger("httpx").level == logging.WARNING