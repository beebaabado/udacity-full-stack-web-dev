"""empty message

Revision ID: 6bf9f68feeff
Revises: b99762f90aa8
Create Date: 2020-09-18 18:57:20.135500

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6bf9f68feeff'
down_revision = 'b99762f90aa8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    
    # add columns but accomodate existing data what does not have column
    # adding new column will create null values/error so set nullable = True
    
    op.add_column('todos', sa.Column('completed', sa.Boolean(), nullable=True))
    
    #Execute sql statement to set column nullable flag to False
    op.execute('UPDATE todos SET completed = FALSE WHERE completed IS NULL;')
    # ### end Alembic commands ###
    
    #add column  set nullable to false
    op.alter_column('todos', sa.Column('completed', sa.Boolean(), nullable=False))


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('todos', 'completed')
    # ### end Alembic commands ###
