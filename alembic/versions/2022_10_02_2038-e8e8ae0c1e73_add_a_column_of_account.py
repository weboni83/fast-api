"""add a column of account

Revision ID: e8e8ae0c1e73
Revises: d3f816667971
Create Date: 2022-10-02 20:38:50.653271

"""
from datetime import datetime, time
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e8e8ae0c1e73'
down_revision = 'd3f816667971'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('insert_at', sa.DateTime(timezone=True), server_default=sa.func.current_timestamp(), nullable=False))
    # how to set default value?
    # following below code (for mysql)
    # op.execute("UPDATE users SET insert_at = NOW()")
    # op.alter_column('users', 'insert_at', nullable=False)


def downgrade() -> None:
    op.drop_column('users', 'insert_at')
