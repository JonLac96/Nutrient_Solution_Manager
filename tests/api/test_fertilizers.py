from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_fertilizer_returns_201() -> None:
    # Arrange: gültiger Request-Body wie ihn die API erwartet
    payload = {
        "name": "API Calcium Nitrate",
        "description": "angelegt über TestClient",
        "ec_effect_per_ml_per_liter": 0.2,
    }

    # Act: HTTP POST, ohne einen echten Server zu starten
    response = client.post("/fertilizers", json=payload)

    # Assert: Router-Status und Response-Schema, nicht LookupError
    assert response.status_code == 201
    body = response.json()
    assert body["name"] == payload["name"]
    assert isinstance(body["id"], int)
    assert body["id"] > 0

def test_get_not_existing_fertilizer_returns_404() -> None:

    # Act: HTTP POST, ohne einen echten Server zu starten
    response = client.get("/fertilizers/99999")

    # Assert: Router-Status und Response-Schema, nicht LookupError
    assert response.status_code == 404
