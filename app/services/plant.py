from sqlalchemy import select
from sqlalchemy.orm import Session
from app.schemas.plant import PlantCreate, PlantUpdate
from app.models.plant import Plant


class PlantService:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get(self, plant_id: int) -> Plant:

        plant = self._session.get(Plant,plant_id)

        if plant is None:
            raise LookupError(f"Plant {plant_id} not found")


        return plant


    def create(self, data: PlantCreate) -> Plant:

        plant = Plant (
            name = data.name,
            description = data.description
        ) 

        self._session.add(plant)
        self._session.commit()
        self._session.refresh(plant)

        return plant

    def update(self, plant_id: int, data: PlantUpdate) -> Plant:

        plant= self.get(plant_id)

        update= data.model_dump(exclude_unset=True)

        for attribut,value in update.items():
            setattr(plant, attribut, value)

        self._session.commit()
        self._session.refresh(plant)

        return plant

    def delete(self, plant_id: int) -> None:

        plant = self.get(plant_id)

        self._session.delete(plant)
        self._session.commit()

    def get_all(self) -> list[Plant]:

        return self._session.scalars(select(Plant)).all()

