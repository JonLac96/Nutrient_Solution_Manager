from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.models.plant import Plant
from app.schemas.plant import PlantCreate, PlantResponse, PlantUpdate
from app.services.plant import PlantService

router = APIRouter(prefix="/plants", tags=["plants"])


@router.post("", response_model=PlantResponse, status_code=201)
def create_plant(
    payload: PlantCreate,
    session: Session = Depends(get_db),
) -> Plant:
    service = PlantService(session)
    return service.create(payload)


@router.get("", response_model=list[PlantResponse])
def get_plant_all(
    session: Session = Depends(get_db)
) -> list[Plant]:
    service = PlantService(session)
    return service.get_all()

@router.get("/{plant_id}", response_model=PlantResponse)
def get_plant(
    plant_id: int,
    session: Session = Depends(get_db)
) -> Plant:
    service = PlantService(session)
    try:
        return service.get(plant_id)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

@router.put("/{plant_id}", response_model=PlantResponse)
def update_plant(
    plant_id: int,
    data: PlantUpdate,
    session: Session = Depends(get_db)
) -> Plant:
    service = PlantService(session)
    try:
        return service.update(plant_id, data)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

@router.delete("/{plant_id}" , status_code=204)
def delete_plant(
    plant_id: int,
    session: Session = Depends(get_db)
):
    service = PlantService(session)
    try:
        service.delete(plant_id)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc