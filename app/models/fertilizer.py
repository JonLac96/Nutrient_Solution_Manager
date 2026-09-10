import uuid

from sqlalchemy import Float, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Fertilizer(Base):
    __tablename__ = "fertilizers"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    ec_effect_per_ml_per_liter: Mapped[float] = mapped_column(Float)
