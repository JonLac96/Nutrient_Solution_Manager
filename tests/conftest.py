import pytest


@pytest.fixture
def valid_fertilizer_payload() -> dict[str, str | float]:
    return {
        "name": "Calcium Nitrate",
        "description": "Hauptquelle für Calcium und Nitrat",
        "ec_effect_per_ml_per_liter": 0.2,
    }


@pytest.fixture
def valid_plantcreate_payload() -> dict[str, str | float]:
    return {
        "name": "Strawberry",
        "description": "Fruit",
    }
