from pydantic import BaseModel, ConfigDict, Field


class FertilizerCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str | None = None
    ec_effect_per_ml_per_liter: float = Field(gt=0)


class FertilizerUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = None
    ec_effect_per_ml_per_liter: float | None = Field(default=None, gt=0)


class FertilizerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    ec_effect_per_ml_per_liter: float
