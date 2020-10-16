"""add cascade all and delete orphans to artists and albums


Revision ID: 1bf606d10c86
Revises: f78a1c7989ef
Create Date: 2020-10-15 13:19:00.485314

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1bf606d10c86'
down_revision = 'f78a1c7989ef'
branch_labels = None
depends_on = None


def upgrade():
    op.create_foreign_key(None, 'album', 'artist', ['artist_id'], ['id'])
    op.create_foreign_key(None, 'show', 'artist', ['artist_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'show', type_='foreignkey')
    op.drop_constraint(None, 'album', type_='foreignkey')
    # ### end Alembic commands ###