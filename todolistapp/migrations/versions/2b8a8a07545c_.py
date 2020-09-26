"""empty message

Revision ID: 2b8a8a07545c
Revises: 4c7c37c86081
Create Date: 2020-09-25 10:17:03.420077

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2b8a8a07545c'
down_revision = '4c7c37c86081'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('todos', sa.Column('list_id', sa.Integer(), nullable=False))
    op.drop_constraint('todos_todolist_id_fkey', 'todos', type_='foreignkey')
    op.create_foreign_key(None, 'todos', 'todolist', ['list_id'], ['id'])
    op.drop_column('todos', 'todolist_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('todos', sa.Column('todolist_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'todos', type_='foreignkey')
    op.create_foreign_key('todos_todolist_id_fkey', 'todos', 'todolist', ['todolist_id'], ['id'])
    op.drop_column('todos', 'list_id')
    # ### end Alembic commands ###
