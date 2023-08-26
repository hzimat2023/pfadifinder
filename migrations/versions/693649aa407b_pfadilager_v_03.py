"""pfadilager v.03

Revision ID: 693649aa407b
Revises: 307a5dd30cda
Create Date: 2023-08-27 01:21:09.234691

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '693649aa407b'
down_revision = '307a5dd30cda'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pfadilager',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('datum', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('pfadi_lager')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pfadi_lager',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', mysql.VARCHAR(collation='utf8mb3_bin', length=100), nullable=False),
    sa.Column('datum', mysql.VARCHAR(collation='utf8mb3_bin', length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb3_bin',
    mysql_default_charset='utf8mb3',
    mysql_engine='InnoDB'
    )
    op.drop_table('pfadilager')
    # ### end Alembic commands ###