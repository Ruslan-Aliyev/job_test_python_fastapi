"""create test table

Revision ID: 71c567ac6d6e
Revises: 
Create Date: 2023-10-02 19:45:12.155965

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '71c567ac6d6e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "test_table",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("thing", sa.String(5), unique=True, nullable=True)
    )


def downgrade() -> None:
    op.drop_table("test_table")
