"""allow custom txnids

Revision ID: 4ab13a0bd1aa
Revises: 9cb1089a9def
Create Date: 2023-09-07 16:54:12.274305

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4ab13a0bd1aa'
down_revision = '9cb1089a9def'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('transactions', schema=None) as batch_op:
        batch_op.alter_column('txn_id',
               existing_type=sa.UUID(),
               type_=sa.String(length=36),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('transactions', schema=None) as batch_op:
        batch_op.alter_column('txn_id',
               existing_type=sa.String(length=36),
               type_=sa.UUID(),
               existing_nullable=False)

    # ### end Alembic commands ###
