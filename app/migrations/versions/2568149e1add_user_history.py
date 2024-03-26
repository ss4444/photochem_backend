"""user_history

Revision ID: 2568149e1add
Revises: edbe74e2be4e
Create Date: 2024-02-15 14:31:16.970703

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "2568149e1add"
down_revision = "edbe74e2be4e"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "requests",
        sa.Column("id", sa.CHAR(32), nullable=False),
        sa.Column("user_id", sa.CHAR(32), nullable=False),
        sa.Column("mol_formula", sa.String(length=100), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("mol_weight", sa.Float(), nullable=False),
        sa.Column("smiles", sa.String(length=100), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("requests")
