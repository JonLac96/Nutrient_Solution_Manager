from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.models.fertilizer import Fertilizer
from app.schemas.fertilizer import FertilizerCreate, FertilizerResponse
from app.services.fertilizer import FertilizerService

router = APIRouter(prefix="/fertilizers", tags=["fertilizers"])


@router.post("", response_model=FertilizerResponse, status_code=201)
def create_fertilizer(
    payload: FertilizerCreate,
    session: Session = Depends(get_db),
) -> Fertilizer:
    service = FertilizerService(session)
    return service.create(payload)


@router.get("", response_model=list[FertilizerResponse])
def get_fertilizer_all(
    session: Session = Depends(get_db)
) -> list[Fertilizer]:
    service = FertilizerService(session)
    return service.get_all()

@router.get("/{fertilizer_id}", response_model=FertilizerResponse)
def get_fertilizer(
    fertilizer_id: int,
    session: Session = Depends(get_db)
) -> Fertilizer:
    service = FertilizerService(session)
    try:
        return service.get(fertilizer_id)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

@router.put("/{fertilizer_id}", response_model=FertilizerResponse)
def update_fertilizer(
    fertilizer_id: int,
    data: FertilizerUpdate,
    session: Session = Depends(get_db)
) -> Fertilizer:
    service = FertilizerService(session)
    try:
        return service.update(fertilizer_id = fertilizer_id, data = data)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

@router.delete("/{fertilizer_id}")
def delete_fertilizer(
    fertilizer_id: int,
    session: Session = Depends(get_db)
):
    try:
        service.delete(fertilizer_id = fertilizer_id)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from ex
