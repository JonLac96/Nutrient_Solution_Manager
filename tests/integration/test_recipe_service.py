from contextlib import AbstractContextManager
from typing import Callable

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.schemas.growth_stage import GrowthStageCreate
from app.schemas.plant import PlantCreate
from app.schemas.recipe import RecipeCreate, RecipeUpdate
from app.services.recipe import RecipeService


def test_get_raises_lookup_error_when_id_does_not_exist(
    open_session: Callable[[], AbstractContextManager[Session]],
) -> None:
    with open_session() as session:
        service = RecipeService(session)

        with pytest.raises(LookupError):
            service.get(999999)


def test_create_recipe(
    open_session: Callable[[], AbstractContextManager[Session]],
    create_plant: Callable[[Session, PlantCreate], int],
    create_growth_stage: Callable[[Session, GrowthStageCreate], int],
    plant_create_1: PlantCreate,
    grow_stage_create_1: GrowthStageCreate,
    recipe_create_1: RecipeCreate,
) -> None:
    with open_session() as session:
        plant_id = create_plant(session, plant_create_1)
        growth_stage_id = create_growth_stage(
            session,
            grow_stage_create_1.model_copy(update={"plant_id": plant_id}),
        )
        recipe_create = recipe_create_1.model_copy(
            update={"growth_stage_id": growth_stage_id}
        )

        service = RecipeService(session)
        recipe = service.create(recipe_create)

        assert recipe.id is not None
        recipe_id = recipe.id

    with open_session() as session:
        service = RecipeService(session)
        recipe = service.get(recipe_id)

        assert recipe.growth_stage_id == growth_stage_id
        assert recipe.name == recipe_create_1.name


def test_update_recipe(
    open_session: Callable[[], AbstractContextManager[Session]],
    create_plant: Callable[[Session, PlantCreate], int],
    create_growth_stage: Callable[[Session, GrowthStageCreate], int],
    plant_create_1: PlantCreate,
    grow_stage_create_1: GrowthStageCreate,
    recipe_create_1: RecipeCreate,
) -> None:
    with open_session() as session:
        plant_id = create_plant(session, plant_create_1)
        growth_stage_id = create_growth_stage(
            session,
            grow_stage_create_1.model_copy(update={"plant_id": plant_id}),
        )
        recipe_create = recipe_create_1.model_copy(
            update={"growth_stage_id": growth_stage_id}
        )
        service = RecipeService(session)
        recipe = service.create(recipe_create)

        assert recipe.id is not None
        recipe_id = recipe.id

    with open_session() as session:
        service = RecipeService(session)
        service.update(recipe_id, RecipeUpdate(name="Bluete-Mix"))

    with open_session() as session:
        service = RecipeService(session)
        recipe = service.get(recipe_id)

        assert recipe.growth_stage_id == growth_stage_id
        assert recipe.name == "Bluete-Mix"


def test_delete_recipe(
    open_session: Callable[[], AbstractContextManager[Session]],
    create_plant: Callable[[Session, PlantCreate], int],
    create_growth_stage: Callable[[Session, GrowthStageCreate], int],
    plant_create_1: PlantCreate,
    grow_stage_create_1: GrowthStageCreate,
    recipe_create_1: RecipeCreate,
) -> None:
    with open_session() as session:
        plant_id = create_plant(session, plant_create_1)
        growth_stage_id = create_growth_stage(
            session,
            grow_stage_create_1.model_copy(update={"plant_id": plant_id}),
        )
        recipe_create = recipe_create_1.model_copy(
            update={"growth_stage_id": growth_stage_id}
        )
        service = RecipeService(session)
        recipe = service.create(recipe_create)

        assert recipe.id is not None
        recipe_id = recipe.id

    with open_session() as session:
        service = RecipeService(session)
        service.delete(recipe_id)

    with open_session() as session:
        service = RecipeService(session)

        with pytest.raises(LookupError):
            service.get(recipe_id)


def test_second_recipe_for_same_growth_stage_is_rejected(
    open_session: Callable[[], AbstractContextManager[Session]],
    create_plant: Callable[[Session, PlantCreate], int],
    create_growth_stage: Callable[[Session, GrowthStageCreate], int],
    plant_create_1: PlantCreate,
    grow_stage_create_1: GrowthStageCreate,
    recipe_create_1: RecipeCreate,
) -> None:
    with open_session() as session:
        plant_id = create_plant(session, plant_create_1)
        growth_stage_id = create_growth_stage(
            session,
            grow_stage_create_1.model_copy(update={"plant_id": plant_id}),
        )
        recipe_create = recipe_create_1.model_copy(
            update={"growth_stage_id": growth_stage_id}
        )
        service = RecipeService(session)
        service.create(recipe_create)

        with pytest.raises(IntegrityError):
            service.create(recipe_create)
