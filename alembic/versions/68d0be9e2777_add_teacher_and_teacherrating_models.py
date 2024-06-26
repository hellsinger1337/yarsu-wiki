"""Add Teacher and TeacherRating models

Revision ID: 68d0be9e2777
Revises: 88ef200d2cf6
Create Date: 2024-06-23 20:45:30.515410

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '68d0be9e2777'
down_revision: Union[str, None] = '88ef200d2cf6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('teachers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('photo', sa.String(), nullable=True),
    sa.Column('alma_mater', sa.String(), nullable=True),
    sa.Column('degree', sa.String(), nullable=True),
    sa.Column('positions', sa.String(), nullable=True),
    sa.Column('biography', sa.String(), nullable=True),
    sa.Column('knowledge_rating', sa.Float(), nullable=True),
    sa.Column('teaching_skill_rating', sa.Float(), nullable=True),
    sa.Column('communication_rating', sa.Float(), nullable=True),
    sa.Column('easiness_rating', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_teachers_id'), 'teachers', ['id'], unique=False)
    op.create_index(op.f('ix_teachers_name'), 'teachers', ['name'], unique=False)
    op.create_table('teacher_ratings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('teacher_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('knowledge_rating', sa.Float(), nullable=True),
    sa.Column('teaching_skill_rating', sa.Float(), nullable=True),
    sa.Column('communication_rating', sa.Float(), nullable=True),
    sa.Column('easiness_rating', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['teacher_id'], ['teachers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_teacher_ratings_id'), 'teacher_ratings', ['id'], unique=False)
    op.drop_index('ix_users_email', table_name='users')
    op.drop_index('ix_users_id', table_name='users')
    op.drop_index('ix_users_username', table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('username', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('hashed_password', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('avatar', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('is_email_verified', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('verification_token', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('reset_password_token', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='users_pkey')
    )
    op.create_index('ix_users_username', 'users', ['username'], unique=True)
    op.create_index('ix_users_id', 'users', ['id'], unique=False)
    op.create_index('ix_users_email', 'users', ['email'], unique=True)
    op.drop_index(op.f('ix_teacher_ratings_id'), table_name='teacher_ratings')
    op.drop_table('teacher_ratings')
    op.drop_index(op.f('ix_teachers_name'), table_name='teachers')
    op.drop_index(op.f('ix_teachers_id'), table_name='teachers')
    op.drop_table('teachers')
    # ### end Alembic commands ###
