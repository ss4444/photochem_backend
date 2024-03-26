"""create sub table

Revision ID: edbe74e2be4e
Revises: 59115b874b67
Create Date: 2024-02-05 11:37:15.107623

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "edbe74e2be4e"
down_revision = "59115b874b67"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "substances",
        sa.Column("id", sa.CHAR(32), nullable=False),
        sa.Column("user_id", sa.CHAR(32), nullable=False),
        sa.Column("last_name", sa.String(length=100), nullable=False),
        sa.Column("admin_name", sa.String(length=100), nullable=False),
        sa.Column("mol_formula", sa.String(length=100), nullable=False),
        sa.Column("smiles", sa.String(length=1000), nullable=False),
        sa.Column("name", sa.String(length=1000), nullable=False),
        sa.Column("quantity", sa.String(length=100), nullable=True),
        sa.Column("office", sa.String(length=100), nullable=True),
        sa.Column("wardrobe", sa.String(length=100), nullable=True),
        sa.Column("shelf", sa.String(length=100), nullable=True),
        sa.Column("manufacturer", sa.String(length=100), nullable=True),
        sa.Column("purity", sa.String(length=100), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("substances")
