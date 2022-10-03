"""create items table

Revision ID: 85c5a55ac501
Revises: e8e8ae0c1e73
Create Date: 2022-10-03 00:39:51.138876

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '85c5a55ac501'
down_revision = 'e8e8ae0c1e73'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'items',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('title', sa.String(50), unique=True, index=True),
        sa.Column('description', sa.String(200), index=True),
        sa.Column('owner_id', sa.Integer, sa.ForeignKey("users.id")),
    )

def downgrade() -> None:
    op.drop_table('items')
