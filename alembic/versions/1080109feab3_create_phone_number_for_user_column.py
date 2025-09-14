"""Create phone number for user column

Revision ID: 1080109feab3
Revises: 
Create Date: 2025-09-14 19:07:08.216333

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1080109feab3'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable= True))


def downgrade() -> None:
    op.drop_column('users', 'phone_number')