from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.models.recipe import Recipe
from app.schemas.recipe import RecipeCreate, RecipeResponse, RecipeUpdate
from app.services.recipe import RecipeService

router = APIRouter(prefix="/recipes", tags=["recipes"])


@router.post("", response_model=RecipeResponse, status_code=201)
def create_recipe(
    payload: RecipeCreate,
    session: Session = Depends(get_db),
) -> Recipe:
    service = RecipeService(session)
    return service.create(payload)


@router.get("", response_model=list[RecipeResponse])
def get_recipe_all(
    session: Session = Depends(get_db),
) -> list[Recipe]:
    service = RecipeService(session)
    return service.get_all()


@router.get("/{recipe_id}", response_model=RecipeResponse)
def get_recipe(
    recipe_id: int,
    session: Session = Depends(get_db),
) -> Recipe:
    service = RecipeService(session)
    try:
        return service.get(recipe_id)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.put("/{recipe_id}", response_model=RecipeResponse)
def update_recipe(
    recipe_id: int,
    data: RecipeUpdate,
    session: Session = Depends(get_db),
) -> Recipe:
    service = RecipeService(session)
    try:
        return service.update(recipe_id, data)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.delete("/{recipe_id}", status_code=204)
def delete_recipe(
    recipe_id: int,
    session: Session = Depends(get_db),
) -> None:
    service = RecipeService(session)
    try:
        service.delete(recipe_id)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
