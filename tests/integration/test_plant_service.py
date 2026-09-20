import pytest

from app.core.database import SessionLocal
from app.services.plant import PlantService


def test_get_raises_lookup_error_when_id_does_not_exist() -> None:
    # Arrange: Service mit einer echten SQLAlchemy-Session
    with SessionLocal() as session:
        service = PlantService(session)

        # Act + Assert: fehlende Id muss LookupError auslösen
        with pytest.raises(LookupError):
            service.get(999999)