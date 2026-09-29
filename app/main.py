from fastapi import FastAPI
from sqlalchemy import text

from app.api.routers.fertilizers import router as router_fertilizer
from app.api.routers.plants import router as router_plant
from app.api.routers.growth_stages import router as router_growth_stage
from app.core.database import engine


app = FastAPI(
    title="Nutrient Solution Manager",
    version="0.1.0",
)
app.include_router(router_fertilizer)
app.include_router(router_plant)
app.include_router(router_growth_stage)

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





