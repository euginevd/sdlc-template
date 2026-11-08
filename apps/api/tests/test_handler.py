import json

from api.handler import handler


def test_health_returns_ok() -> None:
    response = handler({}, None)
    assert response["statusCode"] == 200
    assert json.loads(str(response["body"])) == {"status": "ok"}
