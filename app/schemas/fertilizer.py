from pydantic import BaseModel, Field


class FertilizerCreate(BaseModel):
    name: str = Field(min_length=1)
    description: str | None = None
    ec_effect_per_ml_per_liter: float = Field(gt=0)


class FertilizerResponse(BaseModel):
    name: str
    description: str | None
    ec_effect_per_ml_per_liter: float
