from flask import Blueprint, jsonify, request, g
from app import db
from app.models import Account
from .utils import check_missing_fields, get_resource_by_id, create_resource, update_resource, get_company_id_header

bp = Blueprint('accounts', __name__)

@bp.before_request
def before_request():
    return get_company_id_header()

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
    return create_resource(Account, data, required_fields)

@bp.route('/v1/accounts/<uuid:account_id>', methods=['PUT'])
def update_account(account_id):
    data = request.get_json() or {}
    account = get_resource_by_id(Account, account_id)
    return update_resource(account, data)
