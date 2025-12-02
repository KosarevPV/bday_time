"""Create notification table

Revision ID: 60e8645fc818
Revises: 217370496cb3
Create Date: 2025-11-08 21:48:11.291796

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "60e8645fc818"
down_revision: Union[str, None] = "217370496cb3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "birthday",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=64), nullable=False),
        sa.Column("year", sa.Numeric(precision=4), nullable=False),
        sa.Column("month", sa.Numeric(precision=2), nullable=False),
        sa.Column("day", sa.Numeric(precision=2), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["bday_time.user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="bday_time",
    )
    op.create_table(
        "notification",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("day_1", sa.Boolean(), nullable=False),
        sa.Column("day_3", sa.Boolean(), nullable=False),
        sa.Column("day_7", sa.Boolean(), nullable=False),
        sa.Column("day_14", sa.Boolean(), nullable=False),
        sa.Column("day_30", sa.Boolean(), nullable=False),
        sa.Column("day_90", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["bday_time.user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="bday_time",
    )


def downgrade() -> None:
    op.drop_table("notification", schema="bday_time")
    op.drop_table("birthday", schema="bday_time")
