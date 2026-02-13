"""add partial unique index for active users

Revision ID: d928862e3ea2
Revises: 9a7f5b5ba0a6
Create Date: 2026-02-13 19:04:18.815507

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd928862e3ea2'
down_revision: Union[str, Sequence[str], None] = '9a7f5b5ba0a6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.drop_index('ix_users_email', table_name='users')
    op.execute("""
        CREATE UNIQUE INDEX ix_users_email_active 
        ON users (email) 
        WHERE is_deleted = false
    """)

def downgrade():
    op.drop_index('ix_users_email_active', table_name='users')
    op.create_index('ix_users_email', 'users', ['email'], unique=True)
