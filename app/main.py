from fastapi import FastAPI
from sqlalchemy import text

from app.core.database import engine
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


@app.get("/tanks/{tank_id}")
def read_tank(tank_id: str) -> dict[str, str]:
    return {"tank_id": tank_id}


@app.get("/plants")
def list_plants(name: str | None = None) -> dict[str, str | None]:
    return {"filter_name": name}


@app.post("/fertilizers", response_model=FertilizerResponse)
def create_fertilizer(payload: FertilizerCreate) -> FertilizerResponse:
    return FertilizerResponse(
        name=payload.name,
        description=payload.description,
        ec_effect_per_ml_per_liter=payload.ec_effect_per_ml_per_liter,
    )

