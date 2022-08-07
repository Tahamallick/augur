"""Made events cntrb_id nullable

Revision ID: 11
Revises: 10
Create Date: 2022-08-06 11:59:08.690921

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '11'
down_revision = '10'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('issue_events', 'cntrb_id',
               existing_type=postgresql.UUID(),
               nullable=True,
               schema='augur_data')
    op.alter_column('pull_request_events', 'cntrb_id',
               existing_type=postgresql.UUID(),
               nullable=True,
               schema='augur_data')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('pull_request_events', 'cntrb_id',
               existing_type=postgresql.UUID(),
               nullable=False,
               schema='augur_data')
    op.alter_column('issue_events', 'cntrb_id',
               existing_type=postgresql.UUID(),
               nullable=False,
               schema='augur_data')
    # ### end Alembic commands ###
