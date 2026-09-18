import pytest

from app.core.database import SessionLocal
from app.services.fertilizer import FertilizerService
from app.schemas.fertilizer import FertilizerCreate, FertilizerUpdate



def test_get_raises_lookup_error_when_id_does_not_exist() -> None:
    # Arrange: Service mit einer echten SQLAlchemy-Session
    with SessionLocal() as session:
        service = FertilizerService(session)

        # Act + Assert: fehlende Id muss LookupError auslösen
        with pytest.raises(LookupError):
            service.get(999999)

def test_create_fertilizer():
    # Arrange: FertilizerCreate Data / Service mit einer echten SQLAlchemy-Session
    data = FertilizerCreate(
        name="f1_name",
        description="f1_descr",
        ec_effect_per_ml_per_liter=1.2
    )
    
    # Act
    with SessionLocal() as session:
        service = FertilizerService(session)
        new_fertilizer = service.create(data)
    
        #Assert
        assert new_fertilizer.id is not None
        assert new_fertilizer.name == data.name

    with SessionLocal() as session:
        service = FertilizerService(session)
        fertilizer = service.get(new_fertilizer.id)

        assert fertilizer is not None
        assert fertilizer.name == new_fertilizer.name


def test_update_fertilizer() -> None:

    # Arrange: FertilizerCreate Data / Service mit einer echten SQLAlchemy-Session
    data = FertilizerCreate(
        name="f1_name",
        description="f1_descr",
        ec_effect_per_ml_per_liter=1.2
    )
    
    with SessionLocal() as session:
        service = FertilizerService(session)
        target_fertilizer = service.create(data)
    
    fertilizer_before= target_fertilizer

    data = FertilizerUpdate(
        description="f1_descr_changed",
        ec_effect_per_ml_per_liter=1.5
    )

    with SessionLocal() as session:
        service = FertilizerService(session)

        service.update(target_fertilizer.id, data)

    with SessionLocal() as session:
        service = FertilizerService(session)
        fertilizer_after = service.get(target_fertilizer.id)

        assert fertilizer_after.id == fertilizer_before.id
        assert fertilizer_after.name == fertilizer_before.name
        assert fertilizer_after.description == data.description
        assert fertilizer_after.ec_effect_per_ml_per_liter == data.ec_effect_per_ml_per_liter


def test_delete_fertilizer() -> None:

    # Arrange: FertilizerCreate Data / Service mit einer echten SQLAlchemy-Session
    data = FertilizerCreate(
        name="f1_name",
        description="f1_descr",
        ec_effect_per_ml_per_liter=1.2
    )
    
    with SessionLocal() as session:
        service = FertilizerService(session)
        target_fertilizer = service.create(data)

    with SessionLocal() as session:
        service = FertilizerService(session)
        service.delete(target_fertilizer.id)

    with SessionLocal() as session:
        service = FertilizerService(session)

        with pytest.raises(LookupError):
            service.get(target_fertilizer.id)




    
