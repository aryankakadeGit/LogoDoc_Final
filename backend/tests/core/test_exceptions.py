from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.core.exceptions import AppError, app_error_handler


class TeapotError(AppError):
    code = "TEAPOT"
    status_code = 418
    message = "Default teapot message."


def _client() -> TestClient:
    app = FastAPI()
    app.add_exception_handler(AppError, app_error_handler)

    @app.get("/default")
    def default():
        raise TeapotError()

    @app.get("/custom")
    def custom():
        raise TeapotError("Custom message.")

    @app.get("/base")
    def base():
        raise AppError()

    return TestClient(app)


def test_subclass_default_message_and_status():
    res = _client().get("/default")
    assert res.status_code == 418
    assert res.json() == {"error": {"code": "TEAPOT", "message": "Default teapot message."}}


def test_custom_message_overrides_default_only_for_instance():
    res = _client().get("/custom")
    assert res.json()["error"]["message"] == "Custom message."
    assert TeapotError.message == "Default teapot message."


def test_base_error_is_generic_500():
    res = _client().get("/base")
    assert res.status_code == 500
    assert res.json()["error"]["code"] == "INTERNAL_ERROR"


def test_str_is_message():
    assert str(TeapotError("x")) == "x"