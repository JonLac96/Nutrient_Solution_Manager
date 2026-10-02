from sqlalchemy import Integer, String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class GrowthStage(Base):
    __tablename__ = "growth_stages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    plant_id: Mapped[int] = mapped_column(ForeignKey("plants.id"))
    plant: Mapped["Plant"] = relationship(back_populates="growth_stages")
    recipe: Mapped["Recipe | None"] = relationship(back_populates="growth_stage")
    name: Mapped[str] = mapped_column(String(100))
    sort_order: Mapped[int] = mapped_column(Integer)
    ec_min: Mapped[float] = mapped_column(Float)
    ec_target: Mapped[float] = mapped_column(Float)
    ec_max: Mapped[float] = mapped_column(Float)
    ph_min: Mapped[float] = mapped_column(Float)
    ph_target: Mapped[float] = mapped_column(Float)
    ph_max: Mapped[float] = mapped_column(Float)
