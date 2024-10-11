from flask import Blueprint, request, jsonify
from app import db
from app.models import Student

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = Student.query.filter_by(username=data['username']).first()
    
    if user and user.check_password(data['password']):
        token = user.get_token()
        return jsonify({'token': token, 'role': user.role}), 200
    return jsonify({'error': 'Invalid credentials'}), 401

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user = Student(username=data['username'], role=data['role'])
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully'}), 201
