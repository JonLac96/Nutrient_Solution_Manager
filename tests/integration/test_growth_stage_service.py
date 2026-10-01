from contextlib import AbstractContextManager
from typing import Callable

import pytest

from sqlalchemy.orm import Session
from app.services.growth_stage import GrowthStageService
from app.schemas.plant import PlantCreate
from app.schemas.growth_stage import GrowthStageCreate, GrowthStageUpdate


def test_get_raises_lookup_error_when_id_does_not_exist(
    open_session: Callable[[], AbstractContextManager[Session]],
) -> None:
    # Arrange
    with open_session() as session:
        service = GrowthStageService(session)

        # Act + Assert: fehlende Id muss LookupError auslösen
        with pytest.raises(LookupError):
            service.get(999999)

def test_create_growth_stage(
    open_session: Callable[[], AbstractContextManager[Session]],
    create_plant: Callable[[Session, PlantCreate], int],
    plant_create_1: PlantCreate,
    grow_stage_create_1: GrowthStageCreate,
) -> None:
    with open_session() as session:
        plant_id = create_plant(session, plant_create_1)
        growth_stage_create = grow_stage_create_1.model_copy(update={"plant_id": plant_id})

        service = GrowthStageService(session)
        growth_stage = service.create(growth_stage_create)

        assert growth_stage.id is not None
        growth_stage_id = growth_stage.id

    with open_session() as session:
        service = GrowthStageService(session)
        growth_stage = service.get(growth_stage_id)

        assert growth_stage.plant_id == plant_id


def test_update_growth_stage(
    open_session: Callable[[], AbstractContextManager[Session]],
    create_plant: Callable[[Session, PlantCreate], int],
    grow_stage_create_1: GrowthStageCreate,
) -> None:

    with open_session() as session:
        plant_id_1 = create_plant(session, PlantCreate(name="plant1", description="descr1"))
        growth_stage_create = grow_stage_create_1.model_copy(update={"plant_id": plant_id_1})
        service = GrowthStageService(session)
        growth_stage = service.create(growth_stage_create)

        assert growth_stage.id is not None
        growth_stage_id = growth_stage.id

    with open_session() as session:
        service = GrowthStageService(session)
        growth_stage = service.update(growth_stage_id, GrowthStageUpdate(name="Bluete"))

    with open_session() as session:
        service = GrowthStageService(session)
        growth_stage = service.get(growth_stage_id)

        assert growth_stage.name == "Bluete"

      



