from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.growth_stage import GrowthStage
from app.schemas.growth_stage import GrowthStageCreate, GrowthStageUpdate


class GrowthStageService:
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, data: GrowthStageCreate) -> GrowthStage:

        growth_stage= GrowthStage(
            plant_id = data.plant_id,
            name = data.name,
            sort_order = data.sort_order,
            ec_min = data.ec_min,
            ec_target = data.ec_target,
            ec_max = data.ec_max,
            ph_min = data.ph_min,
            ph_target = data.ph_target,
            ph_max = data.ph_max
        )

        self._session.add(growth_stage)
        self._session.commit()
        self._session.refresh(growth_stage)

        return growth_stage

    def get(self, growth_stage_id: int) -> GrowthStage:
        
        growth_stage = self._session.get(GrowthStage, growth_stage_id)

        if growth_stage is None:
            raise LookupError(f"GrowthStage {growth_stage_id} not found")

        return growth_stage

    def get_all(self) -> list[GrowthStage]:

        return self._session.scalars(select(GrowthStage)).all()

    def update(self, growth_stage_id: int, data: GrowthStageUpdate) -> GrowthStage:

        growth_stage = self.get(growth_stage_id)

        for key,value in data.model_dump(exclude_unset=True).items():
            setattr(growth_stage, key, value)

        self._session.commit()
        self._session.refresh(growth_stage)

        return growth_stage

    def delete(self, growth_stage_id: int) -> None:

        growth_stage = self.get(growth_stage_id)

        self._session.delete(growth_stage)
        self._session.commit()