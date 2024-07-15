"""Add TeacherRequest table

Revision ID: 85bfa5d82569
Revises: 9ba63bf2e900
Create Date: 2024-07-14 13:23:21.300581

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '85bfa5d82569'
down_revision: Union[str, None] = '9ba63bf2e900'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('teacher_requests',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('photo', sa.String(), nullable=True),
    sa.Column('alma_mater', sa.String(), nullable=True),
    sa.Column('degree', sa.String(), nullable=True),
    sa.Column('positions', sa.String(), nullable=True),
    sa.Column('biography', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('is_approved', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_teacher_requests_id'), 'teacher_requests', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_teacher_requests_id'), table_name='teacher_requests')
    op.drop_table('teacher_requests')
    # ### end Alembic commands ###
