"""empty message

Revision ID: 07e036de8ad0
Revises: 5cdffae8817d
Create Date: 2023-06-27 16:51:24.265882

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = '07e036de8ad0'
down_revision = '5cdffae8817d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('resumes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('completion_percentage', sa.SMALLINT(), nullable=False, default=0))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('resumes', schema=None) as batch_op:
        batch_op.drop_column('completion_percentage')

    # ### end Alembic commands ###
