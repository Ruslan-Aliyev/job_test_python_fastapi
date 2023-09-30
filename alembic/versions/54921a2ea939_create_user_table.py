"""create user table

Revision ID: 54921a2ea939
Revises: 46fc579506e1
Create Date: 2023-10-01 05:00:29.271046

"""
from typing import Sequence, Union
from sqlalchemy import func
from sqlalchemy.schema import Sequence as Seq, CreateSequence as CreateSeq
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '54921a2ea939'
down_revision: Union[str, None] = '46fc579506e1'
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
