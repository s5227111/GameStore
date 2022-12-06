"""added user cart table and more columns for my_games

Revision ID: bc7d3fd14654
Revises: 93b0df6c3bab
Create Date: 2022-12-06 19:03:48.419824

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bc7d3fd14654'
down_revision = '93b0df6c3bab'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_cart',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('game_id', sa.Integer(), nullable=True),
    sa.Column('added_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('game_id')
    )
    op.add_column('my_games', sa.Column('added_at', sa.DateTime(), nullable=True))
    op.add_column('my_games', sa.Column('is_downloaded', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('my_games', 'is_downloaded')
    op.drop_column('my_games', 'added_at')
    op.drop_table('user_cart')
    # ### end Alembic commands ###
