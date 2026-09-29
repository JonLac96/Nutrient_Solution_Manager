from typing import Callable

import pytest

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.schemas.plant import PlantCreate
from app.services.plant import PlantService

@pytest.fixture
def session() -> Session:
    with SessionLocal() as session:
        yield session


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


@pytest.fixture
def existing_plant_id() -> int:
    with SessionLocal() as session:
        service = PlantService(session)
        plant = service.create(
            PlantCreate(name="Fixture Plant", description="Nur für Tests angelegt")
        )
        return plant.id


@pytest.fixture
def create_plant(session: Session) -> Callable[[PlantCreate], int]:
    def _make(plant_create: PlantCreate) -> int:
        service = PlantService(session)
        plant = service.create(plant_create)
        return plant.id
    return _make


@pytest.fixture
def plant1(create_plant: Callable[[PlantCreate], int]) -> int:
    return create_plant(PlantCreate(name="test", description="test"))


@pytest.fixture
def valid_growth_stage_payload(
    existing_plant_id: int,
) -> dict[str, str | int | float]:
    return {
        "plant_id": existing_plant_id,
        "name": "Vegetative",
        "sort_order": 1,
        "ec_min": 1.0,
        "ec_target": 1.5,
        "ec_max": 2.0,
        "ph_min": 5.5,
        "ph_target": 6.0,
        "ph_max": 6.5,
    }
