"""create users table

Revision ID: d3471febd252
Revises: 71c567ac6d6e
Create Date: 2023-10-02 19:45:49.928755

"""
from typing import Sequence, Union
from sqlalchemy import func
from sqlalchemy.schema import Sequence as Seq, CreateSequence as CreateSeq
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd3471febd252'
down_revision: Union[str, None] = '71c567ac6d6e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(CreateSeq(Seq('groups_field_seq')))

    op.create_table(
        "users",
        sa.Column("id", sa.Integer, Seq('group_id_seq'), primary_key=True),
        sa.Column("username", sa.String(100), unique=True, nullable=False),
        sa.Column("password", sa.String(100), unique=False, nullable=False),
        sa.Column("birthday", sa.Date(), unique=False, nullable=False),
        sa.Column("create_time", sa.TIMESTAMP(timezone=True), nullable=False, server_default=func.now()),
        sa.Column("last_login", sa.TIMESTAMP(timezone=True), nullable=True)
    )


def downgrade() -> None:
    op.drop_table("users")
