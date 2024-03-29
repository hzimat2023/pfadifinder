"""users table

Revision ID: 477a62eae029
Revises: 
Create Date: 2023-08-28 12:48:48.562720

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '477a62eae029'
down_revision = None
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
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('vorname', sa.String(length=64), nullable=True),
    sa.Column('nachname', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('role', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_user_username'), ['username'], unique=True)

    op.create_table('pfadikind',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('pfadiname', sa.String(length=64), nullable=True),
    sa.Column('vegetarisch', sa.Boolean(), nullable=True),
    sa.Column('vorname', sa.String(length=64), nullable=True),
    sa.Column('nachname', sa.String(length=64), nullable=True),
    sa.Column('geburtsdatum', sa.Date(), nullable=True),
    sa.Column('adresse', sa.String(length=128), nullable=True),
    sa.Column('telefonprivat', sa.String(length=20), nullable=True),
    sa.Column('telefonberuflich', sa.String(length=20), nullable=True),
    sa.Column('allergien_unvertraeglichkeiten', sa.Text(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pfadilageranmeldung',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('pfadilager_id', sa.Integer(), nullable=False),
    sa.Column('datum', sa.String(length=50), nullable=False),
    sa.Column('vorname', sa.String(length=64), nullable=True),
    sa.Column('nachname', sa.String(length=64), nullable=True),
    sa.Column('pfadikind_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['pfadikind_id'], ['pfadikind.id'], ),
    sa.ForeignKeyConstraint(['pfadilager_id'], ['pfadilager.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pfadilageranmeldung')
    op.drop_table('pfadikind')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_username'))
        batch_op.drop_index(batch_op.f('ix_user_email'))

    op.drop_table('user')
    op.drop_table('pfadilager')
    # ### end Alembic commands ###
