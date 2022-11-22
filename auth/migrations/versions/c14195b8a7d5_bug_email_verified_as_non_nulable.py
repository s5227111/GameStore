"""bug email_verified as non nulable

Revision ID: c14195b8a7d5
Revises: fe62f4479367
Create Date: 2022-11-22 19:14:17.449469

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c14195b8a7d5'
down_revision = 'fe62f4479367'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column('users', 'is_email_verified')


def downgrade() -> None:
    op.add_column('users', sa.Column('is_email_verified', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
