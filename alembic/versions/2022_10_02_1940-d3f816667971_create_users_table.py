"""create users table

Revision ID: d3f816667971
Revises: 
Create Date: 2022-10-02 19:40:44.482390

"""
from email.policy import default
from enum import unique
from operator import index
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd3f816667971'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('email', sa.VARCHAR(320), unique=True, index=True),
        sa.Column('hashed_password', sa.VARCHAR(128)),
        sa.Column('is_active', sa.Boolean, default=True),
    )


def downgrade() -> None:
    op.drop_table('users')
