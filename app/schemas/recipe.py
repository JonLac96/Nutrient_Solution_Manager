from pydantic import BaseModel, ConfigDict, Field


class RecipeCreate(BaseModel):
    growth_stage_id: int
    name: str = Field(min_length=1, max_length=100)


class RecipeUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)


class RecipeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    growth_stage_id: int
    name: str
