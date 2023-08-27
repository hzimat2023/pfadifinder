"""Pfadilageranmeldung v0.1

Revision ID: da807f5aef8f
Revises: 35e5b0776dda
Create Date: 2023-08-27 02:54:03.608433

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da807f5aef8f'
down_revision = '35e5b0776dda'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pfadilageranmeldung', schema=None) as batch_op:
        batch_op.add_column(sa.Column('datum', sa.String(length=50), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pfadilageranmeldung', schema=None) as batch_op:
        batch_op.drop_column('datum')

    # ### end Alembic commands ###
