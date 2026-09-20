from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.fertilizer import Fertilizer
from app.schemas.fertilizer import FertilizerCreate, FertilizerUpdate


class FertilizerService:
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, data: FertilizerCreate) -> Fertilizer:
        fertilizer = Fertilizer(
            name=data.name,
            description=data.description,
            ec_effect_per_ml_per_liter=data.ec_effect_per_ml_per_liter,
        )
        self._session.add(fertilizer)
        self._session.commit()
        self._session.refresh(fertilizer)
        
        return fertilizer

    def get(self, fertilizer_id: int) -> Fertilizer:
        
        fertilizer = self._session.get(Fertilizer, fertilizer_id)

        if fertilizer is None:
            raise LookupError(f"Fertilizer {fertilizer_id} not found")
        return fertilizer

    def get_all(self) -> list[Fertilizer]:

        return self._session.scalars(select(Fertilizer)).all()

    def update(self, fertilizer_id : int, data: FertilizerUpdate) -> Fertilizer:

        fertilizer = self.get(fertilizer_id)

        updates = data.model_dump(exclude_unset=True)

        for attribute,value in updates.items():
                setattr(fertilizer, attribute, value)

        self._session.commit()
        self._session.refresh(fertilizer)
        return fertilizer

    def delete(self, fertilizer_id: int) -> None:

        fertilizer = self.get(fertilizer_id)

        self._session.delete(fertilizer)
        self._session.commit()




        




  
            
