from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_growth_stage_returns_201(
    valid_plantcreate_payload: dict[str, str | float],
    valid_growth_stage_payload: dict[str, str | int | float],
) -> None:
    # Die Growth Stage braucht eine existierende Pflanze. Der Fremdschlüssel
    # wird über die API angelegt, nicht über den Service.
    plant_response = client.post("/plants", json=valid_plantcreate_payload)
    assert plant_response.status_code == 201
    plant_id = plant_response.json()["id"]

    # Kopie, damit die Fixture valid_growth_stage_payload unverändert bleibt.
    payload = valid_growth_stage_payload.copy()
    payload["plant_id"] = plant_id

    response = client.post("/growth-stages", json=payload)

    assert response.status_code == 201
    body = response.json()
    assert body["name"] == payload["name"]
    assert body["plant_id"] == plant_id
    assert isinstance(body["id"], int)
    assert body["id"] > 0


def test_get_not_existing_growth_stage_returns_404() -> None:
    # Der Router übersetzt LookupError in HTTP 404.
    response = client.get("/growth-stages/999999")

    assert response.status_code == 404
