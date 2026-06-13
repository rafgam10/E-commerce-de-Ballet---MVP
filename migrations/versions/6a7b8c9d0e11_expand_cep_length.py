"""Expand CEP length.

Revision ID: 6a7b8c9d0e11
Revises: 5f6c7d8e9a10
Create Date: 2026-06-13 00:00:00.000000

"""

from alembic import op
import sqlalchemy as sa


revision = "6a7b8c9d0e11"
down_revision = "5f6c7d8e9a10"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("enderecos", schema=None) as batch_op:
        batch_op.alter_column(
            "cep",
            existing_type=sa.String(length=8),
            type_=sa.String(length=9),
            existing_nullable=False,
        )


def downgrade():
    with op.batch_alter_table("enderecos", schema=None) as batch_op:
        batch_op.alter_column(
            "cep",
            existing_type=sa.String(length=9),
            type_=sa.String(length=8),
            existing_nullable=False,
        )
