from pydantic import ValidationError
import pytest

from app.schemas.growth_stage import GrowthStageCreate


def test_growth_stage_create_rejects_empty_name(
    valid_growth_stage_payload: dict[str, str | int | float],
) -> None:
    # Arrange: gültige Basis, nur den Namen ungültig machen
    payload = valid_growth_stage_payload.copy()
    payload["name"] = ""

    # Act + Assert: Validierung muss scheitern
    with pytest.raises(ValidationError):
        GrowthStageCreate.model_validate(payload)

def test_growth_stage_create_rejects_negative_ec_min(
    valid_growth_stage_payload: dict[str, str | int | float],
) -> None:
    # Arrange: gültige Basis, nur ec_min ungültig machen
    payload = valid_growth_stage_payload.copy()
    payload["ec_min"] = -1.3

    # Act + Assert: Validierung muss scheitern
    with pytest.raises(ValidationError):
        GrowthStageCreate.model_validate(payload)