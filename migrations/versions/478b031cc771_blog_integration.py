"""blog integration

Revision ID: 478b031cc771
Revises: d4d9dedcf45c
Create Date: 2024-10-23 19:33:52.676888

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '478b031cc771'
down_revision: Union[str, None] = 'd4d9dedcf45c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
