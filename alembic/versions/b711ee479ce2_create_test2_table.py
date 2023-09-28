"""create test2 table

Revision ID: b711ee479ce2
Revises: e5690bbd7b3f
Create Date: 2023-09-28 15:00:33.158347

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b711ee479ce2'
down_revision: Union[str, None] = 'e5690bbd7b3f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "test_table_two",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("thing", sa.String(5), unique=True, nullable=True)
    )


def downgrade() -> None:
    op.drop_table("test_table")
