from tests.api.conftest import error_code


def test_health_ok_without_ai(client_factory):
    response = client_factory(with_ai=False).get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_unknown_route_uses_error_shape(client_factory):
    response = client_factory().get("/api/nope")
    assert response.status_code == 404
    assert error_code(response) == "NOT_FOUND"


def test_wrong_method_uses_error_shape(client_factory):
    response = client_factory().get("/api/logo/analyze")
    assert response.status_code == 405
    assert error_code(response) == "METHOD_NOT_ALLOWED"