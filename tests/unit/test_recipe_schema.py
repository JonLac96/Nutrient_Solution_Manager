from pydantic import ValidationError
import pytest

from app.schemas.recipe import RecipeCreate


def test_recipe_create_rejects_empty_name(
    valid_recipe_payload: dict[str, str | int],
) -> None:
    payload = valid_recipe_payload.copy()
    payload["name"] = ""

    with pytest.raises(ValidationError):
        RecipeCreate.model_validate(payload)
