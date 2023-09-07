"""initial db

Revision ID: b94a2128932b
Revises: 
Create Date: 2023-09-04 17:09:07.050043

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'b94a2128932b'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('accounts',
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('number', sa.Integer(), nullable=False),
        sa.Column('normal', sa.Integer(), nullable=False),
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('company_id', sa.Uuid(), nullable=False),
        sa.Column('date_created', sa.DateTime(), nullable=True),
        sa.Column('date_updated', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('transactions',
        sa.Column('txn_id', sa.Integer(), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('amount', sa.BigInteger(), nullable=False),
        sa.Column('currency', sa.String(length=8), nullable=False),
        sa.Column('account_id', sa.Uuid(), nullable=False),
        sa.Column('account_number', sa.Integer(), nullable=False),
        sa.Column('direction', sa.Integer(), nullable=False),
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('company_id', sa.Uuid(), nullable=False),
        sa.Column('date_created', sa.DateTime(), nullable=True),
        sa.Column('date_updated', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['account_id'], ['accounts.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():

    op.drop_table('transactions')
    op.drop_table('accounts')
    
