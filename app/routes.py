from flask import Blueprint, jsonify, request
from app import db
from app.models import Account, Transaction

bp = Blueprint('routes', __name__)

# # Budget views
# @bp.route('/v1/budgets/', methods=['GET'])
# def get_budgets():
#     headers_lower = {k.lower(): v for k, v in request.headers.items()}
#     company_id = headers_lower.get('company-id')
    
#     if not company_id:
#         return "Invalid or missing company-id header", 400
    
#     budgets = Budget.query.filter_by(company_id=company_id).all()
        
#     return jsonify([budget.to_dict() for budget in budgets])


# @bp.route('/v1/budgets/<uuid:budget_id>', methods=['GET'])
# def get_budget(budget_id):
#     headers_lower = {k.lower(): v for k, v in request.headers.items()}
#     company_id = headers_lower.get('company-id')
    
#     if not company_id:
#         return "Invalid or missing company-id header", 400
    
#     budget = Budget.query.filter_by(id=budget_id, company_id=company_id).first_or_404()
#     return jsonify(budget.to_dict())

# @bp.route('/v1/budgets/', methods=['POST'])
# def create_budget():
#     headers_lower = {k.lower(): v for k, v in request.headers.items()}
#     company_id = headers_lower.get('company-id')
    
#     if not company_id:
#         return "Invalid or missing company-id header", 400
    
#     data = request.get_json() or {}
#     budget = Budget(name=data['name'], company_id=company_id, max_amount=data['max_amount'], is_template=data['is_template'],)
#     db.session.add(budget)
#     db.session.commit()
#     return jsonify(budget.to_dict()), 201

# @bp.route('/v1/budgets/<uuid:budget_id>', methods=['PUT'])
# def update_budget(budget_id):
#     headers_lower = {k.lower(): v for k, v in request.headers.items()}
#     company_id = headers_lower.get('company-id')
    
#     if not company_id:
#         return "Invalid or missing company-id header", 400
    
#     budget = Budget.query.filter_by(id=budget_id, company_id=company_id).first_or_404()
#     data = request.get_json() or {}
#     budget.name = data.get('name', budget.name)
#     budget.max_amount = data.get('max_amount', budget.max_amount)
#     budget.is_template = data.get('is_template', budget.is_template)
#     db.session.commit()
#     return jsonify(budget.to_dict())

# @bp.route('/v1/budgets/<uuid:budget_id>', methods=['DELETE'])
# def delete_budget(budget_id):
#     headers_lower = {k.lower(): v for k, v in request.headers.items()}
#     company_id = headers_lower.get('company-id')
    
#     if not company_id:
#         return "Invalid or missing company-id header", 400
    
#     # Delete all subcategories of the budget
#     subcategories = Subcategory.query.filter_by(company_id=company_id, budget_id=budget_id).all()
#     db.session.delete(subcategories)

#     # Delete all categories of the budget
#     categories = Category.query.filter_by(company_id=company_id, budget_id=budget_id).all()
#     db.session.delete(categories)
    
#     budget = Budget.query.filter_by(id=budget_id, company_id=company_id).first_or_404()
#     db.session.delete(budget)
#     db.session.commit()
#     return '', 204

# # Category views
# @bp.route('/v1/categories/', methods=['GET'])
# def get_categories():
#     headers_lower = {k.lower(): v for k, v in request.headers.items()}
#     company_id = headers_lower.get('company-id')
#     budget_id = headers_lower.get('budget-id')
    
#     if not company_id:
#         return "Invalid or missing company-id or header", 400
    
#     category_query = Category.query.filter_by(company_id=company_id)
    
#     if budget_id:
#         category_query = category_query.filter_by(budget_id=budget_id)
        
#     categories = category_query.all()
#     return jsonify([category.to_dict() for category in categories])

# @bp.route('/v1/categories/<uuid:category_id>', methods=['GET'])
# def get_category(category_id):
#     headers_lower = {k.lower(): v for k, v in request.headers.items()}
#     company_id = headers_lower.get('company-id')
    
#     if not company_id:
#         return "Invalid or missing company-id header", 400
    
#     category = Category.query.filter_by(id=category_id, company_id=company_id).first_or_404()
#     return jsonify(category.to_dict())

# @bp.route('/v1/categories/', methods=['POST'])
# def create_category():
#     headers_lower = {k.lower(): v for k, v in request.headers.items()}
#     company_id = headers_lower.get('company-id')
    
#     if not company_id:
#         return "Invalid or missing company-id header", 400
    
#     data = request.get_json() or {}
#     category = Category(name=data['name'], budget_id=data['budget_id'])
#     db.session.add(category)
#     db.session.commit()
#     return jsonify(category.to_dict()), 201

# @bp.route('/v1/categories/<uuid:category_id>', methods=['PUT'])
# def update_category(category_id):
#     headers_lower = {k.lower(): v for k, v in request.headers.items()}
#     company_id = headers_lower.get('company-id')
    
#     if not company_id:
#         return "Invalid or missing company-id header", 400
    
#     category = Category.query.filter_by(id=category_id, company_id=company_id).first_or_404()
#     data = request.get_json() or {}
#     category.name = data.get('name', category.name)
#     db.session.commit()
#     return jsonify(category.to_dict())

# @bp.route('/v1/categories/<uuid:category_id>', methods=['DELETE'])
# def delete_category(category_id):
#     headers_lower = {k.lower(): v for k, v in request.headers.items()}
#     company_id = headers_lower.get('company-id')
    
#     if not company_id:
#         return "Invalid or missing company-id header", 400
    
#     category = Category.query.filter_by(id=category_id, company_id=company_id).first_or_404()
#     db.session.delete(category)
#     db.session.commit()
#     return '', 204

# # Subcategory views
# @bp.route('/v1/subcategories/', methods=['GET'])
# def get_subcategories():
#     headers_lower = {k.lower(): v for k, v in request.headers.items()}
#     company_id = headers_lower.get('company-id')
#     budget_id = request.headers.get('budget_id')
    
#     if not company_id:
#         return "Invalid or missing company-id header", 400
    
#     subcategory_query = Subcategory.query.filter_by(company_id=company_id)
    
#     if budget_id:
#         subcategory_query = subcategory_query.filter(Category.budget_id == budget_id).join(Category) 
        
#     subcategories = subcategory_query.all()
#     return jsonify([subcategory.to_dict() for subcategory in subcategories])

# @bp.route('/v1/subcategories/<uuid:category_id>', methods=['GET'])
# def get_subcategory(subcategory_id):
#     headers_lower = {k.lower(): v for k, v in request.headers.items()}
#     company_id = headers_lower.get('company-id')
    
#     if not company_id:
#         return "Invalid or missing company-id header", 400
    
#     subcategory = Subcategory.query.filter_by(id=subcategory_id, company_id=company_id).first_or_404()
#     return jsonify(subcategory.to_dict())

# @bp.route('/v1/subcategories/', methods=['POST'])
# def create_subcategory():
#     headers_lower = {k.lower(): v for k, v in request.headers.items()}
#     company_id = headers_lower.get('company-id')
    
#     if not company_id:
#         return "Invalid or missing company-id header", 400
    
#     data = request.get_json() or {}
#     subcategory = Subcategory(name=data['name'], category_id=data['category_id'])
#     db.session.add(subcategory)
#     db.session.commit()
#     return jsonify(subcategory.to_dict()), 201

# @bp.route('/v1/subcategories/<uuid:subcategory_id>', methods=['PUT'])
# def update_subcategory(subcategory_id):
#     headers_lower = {k.lower(): v for k, v in request.headers.items()}
#     company_id = headers_lower.get('company-id')
    
#     if not company_id:
#         return "Invalid or missing company-id header", 400
    
#     subcategory = Subcategory.query.filter_by(id=subcategory_id, company_id=company_id).first_or_404()
#     data = request.get_json() or {}
#     subcategory.name = data.get('name', subcategory.name)
#     db.session.commit()
#     return jsonify(subcategory.to_dict())

# @bp.route('/v1/subcategories/<uuid:subcategory_id>', methods=['DELETE'])
# def delete_subcategory(subcategory_id):
#     headers_lower = {k.lower(): v for k, v in request.headers.items()}
#     company_id = headers_lower.get('company-id')
    
#     if not company_id:
#         return "Invalid or missing company-id header", 400
    
#     subcategory = Subcategory.query.filter_by(id=subcategory_id, company_id=company_id).first_or_404()
#     db.session.delete(subcategory)
#     db.session.commit()
#     return '', 204
