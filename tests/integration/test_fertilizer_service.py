from contextlib import AbstractContextManager
from typing import Callable

import pytest

from sqlalchemy.orm import Session
from app.services.fertilizer import FertilizerService
from app.schemas.fertilizer import FertilizerCreate, FertilizerUpdate


def test_get_raises_lookup_error_when_id_does_not_exist(
    open_session: Callable[[], AbstractContextManager[Session]],
) -> None:
    # Arrange: Service mit einer eigenen Session
    with open_session() as session:
        service = FertilizerService(session)

        # Act + Assert: fehlende Id muss LookupError auslösen
        with pytest.raises(LookupError):
            service.get(999999)


def test_create_fertilizer(
    open_session: Callable[[], AbstractContextManager[Session]],
) -> None:
    # Arrange: FertilizerCreate Data
    data = FertilizerCreate(
        name="f1_name",
        description="f1_descr",
        ec_effect_per_ml_per_liter=1.2
    )

    # Act
    with open_session() as session:
        service = FertilizerService(session)
        new_fertilizer = service.create(data)

        # Assert
        assert new_fertilizer.id is not None
        assert new_fertilizer.name == data.name

    with open_session() as fresh_session:
        service = FertilizerService(fresh_session)
        fertilizer = service.get(new_fertilizer.id)

        assert fertilizer is not None
        assert fertilizer.name == new_fertilizer.name


def test_update_fertilizer(
    open_session: Callable[[], AbstractContextManager[Session]],
) -> None:

    # Arrange: FertilizerCreate Data
    data = FertilizerCreate(
        name="f1_name",
        description="f1_descr",
        ec_effect_per_ml_per_liter=1.2
    )

    with open_session() as session:
        service = FertilizerService(session)
        target_fertilizer = service.create(data)

    fertilizer_before = target_fertilizer

    data = FertilizerUpdate(
        description="f1_descr_changed",
        ec_effect_per_ml_per_liter=1.5
    )

    with open_session() as update_session:
        service = FertilizerService(update_session)
        service.update(target_fertilizer.id, data)

    with open_session() as fresh_session:
        service = FertilizerService(fresh_session)
        fertilizer_after = service.get(target_fertilizer.id)

        assert fertilizer_after.id == fertilizer_before.id
        assert fertilizer_after.name == fertilizer_before.name
        assert fertilizer_after.description == data.description
        assert fertilizer_after.ec_effect_per_ml_per_liter == data.ec_effect_per_ml_per_liter


def test_delete_fertilizer(
    open_session: Callable[[], AbstractContextManager[Session]],
) -> None:

    # Arrange: FertilizerCreate Data
    data = FertilizerCreate(
        name="f1_name",
        description="f1_descr",
        ec_effect_per_ml_per_liter=1.2
    )

    with open_session() as session:
        service = FertilizerService(session)
        target_fertilizer = service.create(data)

    with open_session() as delete_session:
        service = FertilizerService(delete_session)
        service.delete(target_fertilizer.id)

    with open_session() as fresh_session:
        service = FertilizerService(fresh_session)

        with pytest.raises(LookupError):
            service.get(target_fertilizer.id)
