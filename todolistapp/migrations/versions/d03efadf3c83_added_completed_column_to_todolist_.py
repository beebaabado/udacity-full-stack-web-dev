"""added completed column to TodoList table model


Revision ID: d03efadf3c83
Revises: ebd9f915d1be
Create Date: 2020-09-25 21:15:44.441704

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd03efadf3c83'
down_revision = 'ebd9f915d1be'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('todolist', sa.Column('completed', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('todolist', 'completed')
    # ### end Alembic commands ###