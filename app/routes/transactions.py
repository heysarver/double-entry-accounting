from flask import Blueprint, jsonify, request, g
from app import db
from app.models import Transaction
from .utils import get_resource_by_id, create_resource, update_resource, get_company_id_header, execute_query
import logging
import uuid

bp = Blueprint('transactions', __name__)

@bp.before_request
def before_request():
    return get_company_id_header()

# Transaction CRUD
@bp.route('/v1/transactions/', methods=['GET'])
def get_transactions():
    transactions = Transaction.query.filter_by(company_id=g.company_id).all()
    return jsonify([transaction.to_dict() for transaction in transactions])

@bp.route('/v1/transactions/<uuid:transaction_id>', methods=['GET'])
def get_transaction(transaction_id):
    transaction = get_resource_by_id(Transaction, transaction_id)
    return jsonify(transaction.to_dict())

@bp.route('/v1/transactions/', methods=['POST'])
def create_transaction():
    data = request.get_json() or {}

    txn_common = {}
    txn_debit = {}
    txn_credit = {}

    txn_common['txn_id'] = str(uuid.uuid4())
    txn_common['date'] = data['date']
    txn_common['currency'] = data['currency']
    txn_common['amount'] = data['amount']
    
    txn_debit.update(txn_common)
    txn_credit.update(txn_common)

    txn_debit['account_id'] = data['debit_account']
    txn_credit['account_id'] = data['credit_account']
    txn_debit['direction'] = 1
    txn_credit['direction'] = -1

    required_fields = ['account_id', 'amount', 'currency', 'date', 'direction', 'txn_id']

    # Needs error handling badly
    debit = create_resource(Transaction, txn_debit, required_fields)
    credit = create_resource(Transaction, txn_credit, required_fields)

    return jsonify(txn_common.to_dict()), 201

# ## Shouldn't allow updating to keep data integrity, delete then recreate instead
# @bp.route('/v1/transactions/<uuid:transaction_id>', methods=['PUT'])
# def update_transaction(transaction_id):
#     data = request.get_json() or {}
#     transaction = get_resource_by_id(Transaction, transaction_id)
#     return update_resource(transaction, data)

# Read-Only Views
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

@bp.route('/v1/transactions/list', methods=['GET'])
def get_vw_transactions():
    query = """
        SELECT txn_id, date, name, DR, CR
        FROM vw_transactions
        WHERE company_id = %s
        ORDER BY date, txn_id, direction desc;
    """
    return jsonify(execute_query(query))
