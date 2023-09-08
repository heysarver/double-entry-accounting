from flask import Blueprint, jsonify, g
from app import get_db_connection
from .utils import get_company_id_header

bp = Blueprint('views', __name__)

@bp.before_request
def before_request():
    return get_company_id_header()

def execute_query(query):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(query, (g.company_id,))
    res = cur.fetchall()
    col_names = [desc[0] for desc in cur.description]
    data = [dict(zip(col_names, row)) for row in res]
    cur.close()
    conn.close()
    return data

# Read-Only Views
@bp.route('/v1/accounts/expressions/all', methods=['GET'])
def get_vw_account_expressions_all():
    query = """
        SELECT expression 
        FROM vw_account_expressions_all 
        WHERE company_id = %s;
    """
    return jsonify(execute_query(query))

@bp.route('/v1/accounts/expressions/rolled', methods=['GET'])
def get_vw_account_expressions_rolled():
    query = """
        SELECT expression
        FROM vw_account_expressions_rolled
        WHERE company_id = %s;
    """
    return jsonify(execute_query(query))

@bp.route('/v1/accounts/equation', methods=['GET'])
def get_vw_account_equation():
    query = """
        SELECT equation
        FROM vw_account_equation
        WHERE company_id = %s;
    """
    return jsonify(execute_query(query))

@bp.route('/v1/transactions/detail/accounts', methods=['GET'])
def get_vw_transactions_with_accounts():
    query = """
        SELECT
            txn_id,
            date,
            amount,
            currency,
            account_id,
            direction,
            name,
            number,
            normal
        FROM vw_transactions_with_accounts
        WHERE company_id = %s
        ORDER BY date, txn_id, direction desc;
    """
    return jsonify(execute_query(query))

@bp.route('/v1/transactions/sum/dr-cr', methods=['GET'])
def get_vw_dr_cr_sums():
    query = """
        SELECT DR, CR
        FROM vw_dr_cr_sums
        WHERE company_id = %s;
    """
    return jsonify(execute_query(query))

@bp.route('/v1/transactions/sum', methods=['GET'])
def get_vw_total_sum():
    query = """
        SELECT total_sum
        FROM vw_total_sum
        WHERE company_id = %s;
    """
    return jsonify(execute_query(query))

@bp.route('/v1/transactions/sum/non-zero', methods=['GET'])
def get_vw_non_zero_sums():
    query = """
        SELECT txn_id, s
        FROM vw_non_zero_sums
        WHERE company_id = %s;
    """
    return jsonify(execute_query(query))

@bp.route('/v1/accounts/balances', methods=['GET'])
def get_vw_account_balances():
    query = """
        SELECT number, name, balance
        FROM vw_account_balances
        WHERE company_id = %s
        ORDER BY number;
    """
    return jsonify(execute_query(query))

@bp.route('/v1/transactions/list', methods=['GET'])
def get_vw_transactions():
    query = """
        SELECT txn_id, date, name, DR, CR
        FROM vw_transactions
        WHERE company_id = %s
        ORDER BY date, txn_id, direction desc;
    """
    return jsonify(execute_query(query))
