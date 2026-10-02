from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.recipe import Recipe
from app.schemas.recipe import RecipeCreate, RecipeUpdate


class RecipeService:
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, data: RecipeCreate) -> Recipe:
        recipe = Recipe(
            growth_stage_id=data.growth_stage_id,
            name=data.name,
        )

        self._session.add(recipe)
        self._session.commit()
        self._session.refresh(recipe)

        return recipe

    def get(self, recipe_id: int) -> Recipe:
        recipe = self._session.get(Recipe, recipe_id)

        if recipe is None:
            raise LookupError(f"Recipe {recipe_id} not found")

        return recipe

    def get_all(self) -> list[Recipe]:
        return list(self._session.scalars(select(Recipe)).all())

    def update(self, recipe_id: int, data: RecipeUpdate) -> Recipe:
        recipe = self.get(recipe_id)

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(recipe, key, value)

        self._session.commit()
        self._session.refresh(recipe)

        return recipe

    def delete(self, recipe_id: int) -> None:
        recipe = self.get(recipe_id)

        self._session.delete(recipe)
        self._session.commit()
