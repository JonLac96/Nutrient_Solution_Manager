from fastapi import FastAPI
from sqlalchemy import select, text

from app.core.database import SessionLocal, engine
from app.models import DemoRecord
from app.schemas.fertilizer import FertilizerCreate, FertilizerResponse

app = FastAPI(
    title="Nutrient Solution Manager",
    version="0.1.0",
)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"name": "Nutrient Solution Manager"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/health/db")
def health_db() -> dict[str, str]:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    return {"database": "ok"}


@app.get("/demo-records")
def list_demo_records() -> list[dict[str, str]]:
    with SessionLocal() as session:
        records = session.scalars(select(DemoRecord)).all()
        return [{"id": str(record.id), "name": record.name} for record in records]


@app.post("/demo-records")
def create_demo_record(name: str) -> dict[str, str]:
    with SessionLocal() as session:
        record = DemoRecord(name=name)
        session.add(record)
        session.commit()
        session.refresh(record)
        return {"id": str(record.id), "name": record.name}


@app.get("/tanks/{tank_id}")
def read_tank(tank_id: str) -> dict[str, str]:
    return {"tank_id": tank_id}


@app.get("/plants")
def list_plants(name: str | None = None) -> dict[str, str | None]:
    return {"filter_name": name}


@app.post("/fertilizers", response_model=FertilizerResponse)
def create_fertilizer(payload: FertilizerCreate) -> FertilizerResponse:
    return FertilizerResponse(
        id=1,
        name=payload.name,
        description=payload.description,
        ec_effect_per_ml_per_liter=payload.ec_effect_per_ml_per_liter,
    )

