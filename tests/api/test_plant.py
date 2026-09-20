from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_plant_returns_201(
    valid_plantcreate_payload: dict[str, str]
) -> None:
    # Arrange: gültiger Request-Body wie ihn die API erwartet
    payload = valid_plantcreate_payload

    # Act: HTTP POST, ohne einen echten Server zu starten
    response = client.post("/plants", json=payload)

    # Assert: Router-Status und Response-Schema, nicht LookupError
    assert response.status_code == 201
    body = response.json()
    assert body["name"] == payload["name"]
    assert isinstance(body["id"], int)
    assert body["id"] > 0