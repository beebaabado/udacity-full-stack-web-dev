"""empty message

Revision ID: 4c7c37c86081
Revises: 03dbcfaf7f83
Create Date: 2020-09-24 19:52:19.603323

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4c7c37c86081'
down_revision = '03dbcfaf7f83'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('todos', 'todolist_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('todos', 'todolist_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
