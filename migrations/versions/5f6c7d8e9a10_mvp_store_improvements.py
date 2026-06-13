"""MVP store improvements.

Revision ID: 5f6c7d8e9a10
Revises: 2678a7398a88
Create Date: 2026-06-12 00:00:00.000000

"""

from alembic import op
import sqlalchemy as sa


revision = "5f6c7d8e9a10"
down_revision = "2678a7398a88"
branch_labels = None
depends_on = None


def _drop_unique_for_column(table_name, column_name):
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    constraint_names = []
    for constraint in inspector.get_unique_constraints(table_name):
        if column_name in constraint.get("column_names", []) and constraint.get("name"):
            constraint_names.append(constraint["name"])

    with op.batch_alter_table(table_name, schema=None) as batch_op:
        for name in constraint_names:
            batch_op.drop_constraint(name, type_="unique")


def upgrade():
    _drop_unique_for_column("usuarios", "senha")

    with op.batch_alter_table("categorias", schema=None) as batch_op:
        batch_op.create_unique_constraint("uq_categorias_slug", ["slug"])

    with op.batch_alter_table("produtos", schema=None) as batch_op:
        batch_op.create_unique_constraint("uq_produtos_slug", ["slug"])

    with op.batch_alter_table("variavel_produtos", schema=None) as batch_op:
        batch_op.create_unique_constraint("uq_variavel_produtos_sku", ["sku"])

    with op.batch_alter_table("carrinhos", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "status", sa.String(length=20), nullable=False, server_default="ativo"
            )
        )

    with op.batch_alter_table("itens_ordens", schema=None) as batch_op:
        batch_op.alter_column("quantidade", existing_type=sa.Integer(), nullable=False)
        batch_op.add_column(
            sa.Column("nome_produto", sa.String(length=255), nullable=True)
        )
        batch_op.add_column(sa.Column("sku", sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column("tamanho", sa.String(length=10), nullable=True))
        batch_op.add_column(sa.Column("cor", sa.String(length=100), nullable=True))


def downgrade():
    with op.batch_alter_table("itens_ordens", schema=None) as batch_op:
        batch_op.drop_column("cor")
        batch_op.drop_column("tamanho")
        batch_op.drop_column("sku")
        batch_op.drop_column("nome_produto")
        batch_op.alter_column("quantidade", existing_type=sa.Integer(), nullable=True)

    with op.batch_alter_table("carrinhos", schema=None) as batch_op:
        batch_op.drop_column("status")

    with op.batch_alter_table("variavel_produtos", schema=None) as batch_op:
        batch_op.drop_constraint("uq_variavel_produtos_sku", type_="unique")

    with op.batch_alter_table("produtos", schema=None) as batch_op:
        batch_op.drop_constraint("uq_produtos_slug", type_="unique")

    with op.batch_alter_table("categorias", schema=None) as batch_op:
        batch_op.drop_constraint("uq_categorias_slug", type_="unique")

    with op.batch_alter_table("usuarios", schema=None) as batch_op:
        batch_op.create_unique_constraint("uq_usuarios_senha", ["senha"])
