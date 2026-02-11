"""task is_deleted

Revision ID: 444b189c55da
Revises: c8228e4d1686
Create Date: 2026-02-11 18:10:47.427265

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '444b189c55da'
down_revision: Union[str, Sequence[str], None] = 'c8228e4d1686'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # 1. Додаємо колонку як nullable
    op.add_column('tasks', sa.Column('is_deleted', sa.Boolean(), nullable=True))
    
    # 2. Встановлюємо значення False для всіх існуючих записів
    op.execute('UPDATE tasks SET is_deleted = false WHERE is_deleted IS NULL')
    
    # 3. Робимо колонку NOT NULL
    op.alter_column('tasks', 'is_deleted', nullable=False)

def downgrade():
    op.drop_column('tasks', 'is_deleted')