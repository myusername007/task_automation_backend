"""add is_admin

Revision ID: abb31e5c5cc6
Revises: 444b189c55da
Create Date: 2026-02-12 12:34:43.956879

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'abb31e5c5cc6'
down_revision: Union[str, Sequence[str], None] = '444b189c55da'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # 1. Додаємо колонку як nullable
    op.add_column('users', sa.Column('is_admin', sa.Boolean(), nullable=True))
    
    # 2. Встановлюємо значення False для всіх існуючих записів
    op.execute('UPDATE users SET is_admin = false WHERE is_admin IS NULL')
    
    # 3. Робимо колонку NOT NULL
    op.alter_column('users', 'is_admin', nullable=False)

def downgrade():
    op.drop_column('users', 'is_admin')