
from pydantic import ValidationError
import pytest

from app.schemas.plant import PlantCreate


def test_plant_create_rejects_empty_name(
    valid_plantcreate_payload: dict[str, str]
) -> None:
    # Arrange: gültige Basis, nur den Namen ungültig machen
    payload = valid_plantcreate_payload.copy()
    payload["name"] = ""

    # Act + Assert: Validierung muss scheitern
    with pytest.raises(ValidationError):
        PlantCreate.model_validate(payload)