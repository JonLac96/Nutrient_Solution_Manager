from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_recipe_returns_201(
    valid_plantcreate_payload: dict[str, str | float],
    valid_growth_stage_payload: dict[str, str | int | float],
    valid_recipe_payload: dict[str, str | int],
) -> None:
    plant_response = client.post("/plants", json=valid_plantcreate_payload)
    assert plant_response.status_code == 201
    plant_id = plant_response.json()["id"]

    growth_stage_payload = valid_growth_stage_payload.copy()
    growth_stage_payload["plant_id"] = plant_id
    growth_stage_response = client.post("/growth-stages", json=growth_stage_payload)
    assert growth_stage_response.status_code == 201
    growth_stage_id = growth_stage_response.json()["id"]

    payload = valid_recipe_payload.copy()
    payload["growth_stage_id"] = growth_stage_id

    response = client.post("/recipes", json=payload)

    assert response.status_code == 201
    body = response.json()
    assert body["name"] == payload["name"]
    assert body["growth_stage_id"] == growth_stage_id
    assert isinstance(body["id"], int)
    assert body["id"] > 0


def test_get_not_existing_recipe_returns_404() -> None:
    response = client.get("/recipes/999999")

    assert response.status_code == 404
