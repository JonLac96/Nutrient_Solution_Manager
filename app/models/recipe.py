from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Recipe(Base):
    __tablename__ = "recipes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    growth_stage_id: Mapped[int] = mapped_column(ForeignKey("growth_stages.id"), unique=True)
    growth_stage: Mapped["GrowthStage"] = relationship(back_populates="recipe")
    name: Mapped[str] = mapped_column(String(100))
