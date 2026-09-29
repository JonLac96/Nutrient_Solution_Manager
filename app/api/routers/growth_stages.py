from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.models.growth_stage import GrowthStage
from app.schemas.growth_stage import GrowthStageCreate, GrowthStageResponse, GrowthStageUpdate
from app.services.growth_stage import GrowthStageService

router = APIRouter(prefix="/growth-stages", tags=["growth-stages"])


@router.post("", response_model=GrowthStageResponse, status_code=201)
def create_growth_stage(
    payload: GrowthStageCreate,
    session: Session = Depends(get_db),
) -> GrowthStage:
    service = GrowthStageService(session)
    return service.create(payload)


@router.get("", response_model=list[GrowthStageResponse])
def get_growth_stage_all(
    session: Session = Depends(get_db)
) -> list[GrowthStage]:
    service = GrowthStageService(session)
    return service.get_all()

@router.get("/{growth_stage_id}", response_model=GrowthStageResponse)
def get_growth_stage(
    growth_stage_id: int,
    session: Session = Depends(get_db)
) -> GrowthStage:
    service = GrowthStageService(session)
    try:
        return service.get(growth_stage_id)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

@router.put("/{growth_stage_id}", response_model=GrowthStageResponse)
def update_growth_stage(
    growth_stage_id: int,
    data: GrowthStageUpdate,
    session: Session = Depends(get_db)
) -> GrowthStage:
    service = GrowthStageService(session)
    try:
        return service.update(growth_stage_id, data)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

@router.delete("/{growth_stage_id}" , status_code=204)
def delete_growth_stage(
    growth_stage_id: int,
    session: Session = Depends(get_db)
):
    service = GrowthStageService(session)
    try:
        service.delete(growth_stage_id)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc