"""creating phone number column for user table

Revision ID: e482ba21591d
Revises: 
Create Date: 2025-12-27 22:33:10.901829

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e482ba21591d'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users',sa.Column('phone_number', sa.String(),nullable=True))
    pass


def downgrade() -> None:
    op.drop_column('users', 'phone_number')