"""create test table

Revision ID: e5690bbd7b3f
Revises: 
Create Date: 2023-09-28 14:09:28.069817

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e5690bbd7b3f'
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
