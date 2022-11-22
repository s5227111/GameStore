"""bug email_verified as non nulable2

Revision ID: d8189b6f6eab
Revises: c14195b8a7d5
Create Date: 2022-11-22 19:17:14.458616

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd8189b6f6eab'
down_revision = 'c14195b8a7d5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('is_email_verified', sa.Boolean(), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'is_email_verified')
