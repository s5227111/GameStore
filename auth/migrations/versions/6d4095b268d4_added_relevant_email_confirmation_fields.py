"""added relevant email confirmation fields

Revision ID: 6d4095b268d4
Revises: c787756eb104
Create Date: 2022-12-10 01:45:15.200191

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '6d4095b268d4'
down_revision = 'c787756eb104'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('admin', sa.Boolean(), nullable=False))
    op.add_column('users', sa.Column('confirmed', sa.Boolean(), nullable=False))
    op.add_column('users', sa.Column('confirmed_on', sa.DateTime(), nullable=True))
    op.drop_column('users', 'is_email_verified')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('is_email_verified', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
    op.drop_column('users', 'confirmed_on')
    op.drop_column('users', 'confirmed')
    op.drop_column('users', 'admin')
    # ### end Alembic commands ###