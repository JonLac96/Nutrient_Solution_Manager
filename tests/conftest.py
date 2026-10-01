from collections.abc import Iterator
from contextlib import AbstractContextManager, contextmanager
from typing import Callable

import pytest

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.schemas.plant import PlantCreate
from app.services.plant import PlantService
from app.services.growth_stage import GrowthStageCreate

@pytest.fixture
def open_session() -> Callable[[], AbstractContextManager[Session]]:
    @contextmanager
    def _open() -> Iterator[Session]:
        with SessionLocal() as db_session:
            yield db_session

    return _open


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
def valid_growth_stage_payload() -> dict[str, str | int | float]:
    return {
        "plant_id": 1,
        "name": "Vegetative",
        "sort_order": 1,
        "ec_min": 1.2,
        "ec_target": 1.6,
        "ec_max": 2.0,
        "ph_min": 5.5,
        "ph_target": 5.8,
        "ph_max": 6.2,
    }

def plant_create_1() -> PlantCreate:
    return PlantCreate(
        name="plant1",
        description="plant1 descr"
    )

@pytest.fixture
def create_plant(
    open_session: Callable[[], AbstractContextManager[Session]],
) -> Callable[[PlantCreate], int]:
    def _make(plant_create: PlantCreate) -> int:
        with open_session() as session:
            service = PlantService(session)
            plant = service.create(plant_create)
            return plant.id
    return _make


@pytest.fixture
def grow_stage_create_1(
) -> GrowthStageCreate:
    return GrowthStageCreate (
        plant_id=1,
        name="gs1",
        sort_order=1,
        ec_min=4,
        ec_max=6,
        ec_target=5,
        ph_min=4,
        ph_max=6,
        ph_target=5
    )
