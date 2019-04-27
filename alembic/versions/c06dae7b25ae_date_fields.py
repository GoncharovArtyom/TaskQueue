"""date_fields

Revision ID: c06dae7b25ae
Revises: 06bba5b273c7
Create Date: 2019-04-27 15:44:09.407105

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = 'c06dae7b25ae'
down_revision = '06bba5b273c7'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("create extension pgcrypto;")

    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tasks', sa.Column('create_time', sa.DateTime(), nullable=False))
    op.add_column('tasks', sa.Column('execution_time', postgresql.INTERVAL(), nullable=True))
    op.add_column('tasks', sa.Column('start_time', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tasks', 'start_time')
    op.drop_column('tasks', 'execution_time')
    op.drop_column('tasks', 'create_time')
    # ### end Alembic commands ###

    op.execute("drop extension pgcrypto;")
