from flask import Blueprint, jsonify, request, g
from app import db
from app.models import Account, Transaction

bp = Blueprint('routes', __name__)

def check_missing_fields(data, required_fields):
    return [field for field in required_fields if field not in data]

@bp.before_request
def get_company_id_header():
    headers_lower = {k.lower(): v for k, v in request.headers.items()}
    company_id = headers_lower.get('company-id')
    
    if not company_id:
        return "Invalid or missing company-id header", 400
    
    g.company_id = company_id

def get_resource_by_id(resource, resource_id):
    return resource.query.filter_by(id=resource_id, company_id=g.company_id).first_or_404()

# Account CRUD
@bp.route('/v1/accounts/', methods=['GET'])
def get_accounts():
    accounts = Account.query.filter_by(company_id=g.company_id).all()
    return jsonify([account.to_dict() for account in accounts])

@bp.route('/v1/accounts/<uuid:account_id>', methods=['GET'])
def get_account(account_id):
    account = get_resource_by_id(Account, account_id)
    return jsonify(account.to_dict())

@bp.route('/v1/accounts/', methods=['POST'])
def create_account():
    data = request.get_json() or {}

    required_fields = ['name', 'number', 'normal']
    missing_fields = check_missing_fields(data, required_fields)
    if missing_fields:
        return f"Missing required fields: {', '.join(missing_fields)}", 400
    
    account = Account(name=data.get('name'), number=data.get('number'), normal=data.get('normal'), company_id=g.company_id)
    db.session.add(account)
    db.session.commit()
    return jsonify(account.to_dict()), 201

@bp.route('/v1/accounts/<uuid:account_id>', methods=['PUT'])
def update_account(account_id):
    data = request.get_json() or {}
    account = get_resource_by_id(Account, account_id)
    account.name = data.get('name', account.name)
    account.number = data.get('number', account.number)
    account.normal = data.get('normal', account.normal)
    db.session.commit()
    return jsonify(account.to_dict())

@bp.route('/v1/accounts/<uuid:account_id>', methods=['DELETE'])
def delete_account(account_id):
    account = get_resource_by_id(Account, account_id)
    db.session.delete(account)
    return {}, 204

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
    missing_fields = check_missing_fields(data, required_fields)
    if missing_fields:
        return f"Missing required fields: {', '.join(missing_fields)}", 400
    
    transaction = Transaction(
        account_id=data.get('account_id'),
        amount=data.get('amount'),
        currency=data.get('currency'),
        date=data.get('date'),
        direction=data.get('direction'),
        txn_id=data.get('txn_id'),
        company_id=g.company_id)
    db.session.add(transaction)
    db.session.commit()
    return jsonify(transaction.to_dict()), 201

@bp.route('/v1/transactions/<uuid:transaction_id>', methods=['PUT'])
def update_transaction(transaction_id):
    data = request.get_json() or {}
    transaction = get_resource_by_id(Transaction, transaction_id)
    transaction.account_id = data.get('account_id', transaction.account_id)
    transaction.amount = data.get('amount', transaction.amount)
    transaction.currency = data.get('currency', transaction.currency)
    transaction.date = data.get('date', transaction.date)
    transaction.direction = data.get('direction', transaction.direction)
    transaction.txn_id = data.get('txn_id', transaction.txn_id)
    db.session.commit()
    return jsonify(transaction.to_dict())

@bp.route('/v1/transactions/<uuid:transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    transaction = get_resource_by_id(Transaction, transaction_id)
    db.session.delete(transaction)
    return {}, 204
