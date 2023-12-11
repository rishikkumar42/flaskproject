"""Updated Movie model

Revision ID: 684b3b6db145
Revises: 6d5467a5ebaf
Create Date: 2023-12-10 16:59:42.057284

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '684b3b6db145'
down_revision = '6d5467a5ebaf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('movie',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=250), nullable=False),
    sa.Column('release_date', sa.String(length=50), nullable=True),
    sa.Column('vote_average', sa.Float(), nullable=True),
    sa.Column('overview', sa.Text(), nullable=True),
    sa.Column('poster_path', sa.String(length=250), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('movie')
    # ### end Alembic commands ###
