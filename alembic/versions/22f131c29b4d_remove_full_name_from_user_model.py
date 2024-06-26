"""Remove full_name from User model

Revision ID: 22f131c29b4d
Revises: df36de6217b4
Create Date: 2024-06-23 18:13:29.416041

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '22f131c29b4d'
down_revision: Union[str, None] = 'df36de6217b4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'full_name')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('full_name', sa.VARCHAR(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
