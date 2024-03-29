"""empty message

Revision ID: 6f2b4e10c950
Revises: 9eea24e0027d
Create Date: 2022-11-20 15:44:01.591432

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6f2b4e10c950'
down_revision = '9eea24e0027d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('candidates', sa.Column('first_name', sa.String(length=200), nullable=False))
    op.add_column('candidates', sa.Column('last_name', sa.String(length=200), nullable=False))
    op.add_column('candidates', sa.Column('telegram', sa.String(length=200), nullable=False))
    op.drop_column('candidates', 'name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('candidates', sa.Column('name', sa.VARCHAR(length=200), nullable=False))
    op.drop_column('candidates', 'telegram')
    op.drop_column('candidates', 'last_name')
    op.drop_column('candidates', 'first_name')
    # ### end Alembic commands ###
