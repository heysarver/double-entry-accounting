"""add views

Revision ID: 194466430716
Revises: 4ab13a0bd1aa
Create Date: 2023-09-07 17:05:38.914868

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '194466430716'
down_revision = '4ab13a0bd1aa'
branch_labels = None
depends_on = None


def upgrade():

    op.create_index('idx_accounts_number', 'accounts', ['company_id', 'number'], unique=True)
    op.create_index('idx_transactions_account', 'transactions', ['company_id', 'account_id', 'txn_id'], unique=True)

    op.execute("""
        CREATE VIEW vw_account_expressions_all AS
        SELECT
            string_agg(name , ' + ') AS expression,
            company_id
        FROM accounts
        GROUP BY company_id, normal;
    """)
    
    op.execute("""
        CREATE VIEW vw_account_expressions_rolled AS
        SELECT
            string_agg(name, ' + ') AS expression,
            company_id
        FROM accounts
        WHERE number % 100 = 0
        GROUP BY company_id, normal;
    """)

    op.execute("""
        CREATE VIEW vw_account_equation AS
        SELECT
            MAX(left_side) || ' = ' || MAX(right_side) AS equation,
            company_id
        FROM 
            (
                SELECT
                    company_id,
                    STRING_AGG(
                        CASE WHEN normal = 1 THEN name END, ' + '
                    ) AS left_side, 
                    STRING_AGG(
                        CASE WHEN normal = -1 THEN name END, ' + '
                    ) AS right_side 
                FROM accounts 
                WHERE number % 100 = 0 
                GROUP BY company_id, normal
            ) vw
        GROUP BY company_id;
    """)
    
    op.execute("""
        CREATE VIEW vw_transactions_with_accounts AS
        SELECT
            t.txn_id,
            t.date,
            t.amount,
            t.currency,
            t.account_id,
            t.direction,
            a.name,
            a.number,
            a.normal,
            a.company_id
        FROM transactions t
        JOIN accounts a ON t.account_id = a.id AND t.company_id = a.company_id;
    """)

    op.execute("""
        CREATE VIEW vw_dr_cr_sums AS
        SELECT
            SUM(CASE WHEN direction = 1 THEN amount END) AS DR,
            SUM(CASE WHEN direction = -1 THEN amount END) AS CR,
            company_id
        FROM transactions
        GROUP BY company_id;
    """)

    op.execute("""
        CREATE VIEW vw_total_sum AS
        SELECT
            SUM(direction * amount) AS total_sum,
            company_id
        FROM transactions
        GROUP BY company_id;
    """)

    op.execute("""
        CREATE VIEW vw_non_zero_sums AS
        SELECT
            txn_id,
            SUM(direction * amount) AS s,
            company_id
        FROM transactions
        GROUP BY txn_id, company_id
        HAVING SUM(direction * amount) != 0;
    """)

    op.execute("""
        CREATE VIEW vw_account_balances AS
        SELECT
            a.number,
            a.name,
            sum(t.amount * t.direction * a.normal) as balance,
            a.company_id
        FROM transactions t
        JOIN accounts a ON t.account_id = a.id AND t.company_id = a.company_id
        GROUP BY a.company_id, number, name;
    """)

    op.execute("""
    CREATE VIEW vw_transactions AS
        SELECT
            t.txn_id,
            t.date,
            a.name,
            CASE WHEN t.direction = 1 THEN t.amount END AS DR,
            CASE WHEN t.direction = -1 THEN t.amount END AS CR,
            t.direction,
            a.company_id
        FROM
            transactions t
        LEFT JOIN
            accounts a ON t.account_id = a.id;
    """)


def downgrade():
    op.execute("DROP INDEX idx_accounts_number")
    op.execute("DROP INDEX idx_transactions_account")
    op.execute("DROP VIEW vw_account_expressions_all")
    op.execute("DROP VIEW vw_account_expressions_rolled")
    op.execute("DROP VIEW vw_account_equation")
    op.execute("DROP VIEW vw_transactions_with_accounts")
    op.execute("DROP VIEW vw_dr_cr_sums")
    op.execute("DROP VIEW vw_total_sum")
    op.execute("DROP VIEW vw_non_zero_sums")
    op.execute("DROP VIEW vw_account_balances")
    op.execute("DROP VIEW vw_transactions")
