from flask import g, jsonify, request
from app import get_db_connection
from app import db

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

def check_missing_fields(data, required_fields):
    return [field for field in required_fields if field not in data]

def get_resource_by_id(resource, resource_id):
    return resource.query.filter_by(id=resource_id, company_id=g.company_id).first_or_404()

def create_resource(resource, data, required_fields):
    missing_fields = check_missing_fields(data, required_fields)
    if missing_fields:
        return f"Missing required fields: {', '.join(missing_fields)}", 400

    new_resource = resource(**data, company_id=g.company_id)
    db.session.add(new_resource)
    db.session.commit()
    return jsonify(new_resource.to_dict()), 201

def update_resource(resource_instance, data):
    for key, value in data.items():
        setattr(resource_instance, key, value)
    db.session.commit()
    return jsonify(resource_instance.to_dict())

def get_company_id_header():
    headers_lower = {k.lower(): v for k, v in request.headers.items()}
    company_id = headers_lower.get('company-id')
    
    if not company_id:
        return "Invalid or missing company-id header", 400
    
    g.company_id = company_id
