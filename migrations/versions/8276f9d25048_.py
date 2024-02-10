"""empty message

Revision ID: 8276f9d25048
Revises: 29d34a31db35
Create Date: 2023-12-10 14:00:16.766787

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8276f9d25048'
down_revision = '29d34a31db35'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index('email')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index('email', ['email'], unique=False)

    # ### end Alembic commands ###
