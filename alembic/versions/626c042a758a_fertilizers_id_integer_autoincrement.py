"""fertilizers id integer autoincrement

Revision ID: 626c042a758a
Revises: b2741119ca18
Create Date: 2026-09-11 17:12:07.180008

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '626c042a758a'
down_revision: Union[str, Sequence[str], None] = 'b2741119ca18'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Replace UUID primary key with INTEGER autoincrement.

    UUID cannot be cast to INTEGER, so the table is recreated.
    Existing fertilizer rows are dropped.
    """
    op.drop_table("fertilizers")
    op.create_table(
        "fertilizers",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("ec_effect_per_ml_per_liter", sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Restore the UUID primary key from revision b2741119ca18."""
    op.drop_table("fertilizers")
    op.create_table(
        "fertilizers",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("ec_effect_per_ml_per_liter", sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
