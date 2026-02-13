"""user delete

Revision ID: 9a7f5b5ba0a6
Revises: abb31e5c5cc6
Create Date: 2026-02-13 18:45:20.254859

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9a7f5b5ba0a6'
down_revision: Union[str, Sequence[str], None] = 'abb31e5c5cc6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # 1. Додаємо колонку як nullable
    op.add_column('users', sa.Column('is_deleted', sa.Boolean(), nullable=True))
    
    # 2. Встановлюємо значення False для всіх існуючих записів
    op.execute('UPDATE users SET is_deleted = false WHERE is_deleted IS NULL')
    
    # 3. Робимо колонку NOT NULL
    op.alter_column('users', 'is_deleted', nullable=False)

def downgrade():
    op.drop_column('users', 'is_deleted')
