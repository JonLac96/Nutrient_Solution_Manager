from pydantic import ValidationError
import pytest

from app.schemas.fertilizer import FertilizerCreate


def test_fertilizer_create_accepts_valid_data(
    valid_fertilizer_payload: dict[str, str | float],
) -> None:
    # Arrange: gültige Eingabedaten kommen aus der Fixture
    payload = valid_fertilizer_payload

    # Act: Schema validieren und Modell erzeugen
    fertilizer = FertilizerCreate.model_validate(payload)

    # Assert: erwartete Werte prüfen
    assert fertilizer.name == "Calcium Nitrate"
    assert fertilizer.description == "Hauptquelle für Calcium und Nitrat"
    assert fertilizer.ec_effect_per_ml_per_liter == 0.2


def test_fertilizer_create_rejects_empty_name(
    valid_fertilizer_payload: dict[str, str | float],
) -> None:
    # Arrange: gültige Basis, nur den Namen ungültig machen
    payload = valid_fertilizer_payload.copy()
    payload["name"] = ""

    # Act + Assert: Validierung muss scheitern
    with pytest.raises(ValidationError):
        FertilizerCreate.model_validate(payload)


def test_fertilizer_create_rejects_negative_ec_effect(
    valid_fertilizer_payload: dict[str, str | float],
) -> None:
    # Arrange: gültige Basis, nur den EC-Effekt ungültig machen
    payload = valid_fertilizer_payload.copy()
    payload["ec_effect_per_ml_per_liter"] = -2.3

    # Act + Assert: Validierung muss scheitern
    with pytest.raises(ValidationError):
        FertilizerCreate.model_validate(payload)
