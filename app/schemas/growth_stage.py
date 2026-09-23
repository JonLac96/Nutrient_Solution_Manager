from pydantic import BaseModel, ConfigDict, Field


class GrowthStageCreate(BaseModel):
    plant_id: int
    name: str = Field(min_length=1, max_length=100)
    sort_order: int
    ec_min: float = Field(gt=0.0)
    ec_target: float = Field(gt=0.0)
    ec_max: float = Field(gt=0.0)
    ph_min: float = Field(gt=0.0)
    ph_target: float = Field(gt=0.0)
    ph_max: float = Field(gt=0.0)


class GrowthStageUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    sort_order: int | None = None
    ec_min: float | None = Field(default=None, gt=0.0)
    ec_target: float | None = Field(default=None, gt=0.0)
    ec_max: float | None = Field(default=None, gt=0.0)
    ph_min: float | None = Field(default=None, gt=0.0)
    ph_target: float | None = Field(default=None, gt=0.0)
    ph_max: float | None = Field(default=None, gt=0.0)


class GrowthStageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    plant_id: int
    name: str
    sort_order: int
    ec_min: float
    ec_target: float
    ec_max: float
    ph_min: float
    ph_target: float
    ph_max: float
