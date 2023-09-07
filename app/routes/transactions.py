from flask import Blueprint, jsonify, request, g
from app import db
from app.models import Transaction
from .utils import check_missing_fields, get_resource_by_id, create_resource, update_resource, get_company_id_header

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
    required_fields = ['account_id', 'amount', 'currency', 'date', 'direction', 'txn_id']
    return create_resource(Transaction, data, required_fields)

@bp.route('/v1/transactions/<uuid:transaction_id>', methods=['PUT'])
def update_transaction(transaction_id):
    data = request.get_json() or {}
    transaction = get_resource_by_id(Transaction, transaction_id)
    return update_resource(transaction, data)
