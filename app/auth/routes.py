from flask import jsonify, request
from flask_jwt_extended import create_access_token
from app.models import Teacher, Student, Admin
from . import auth_bp

# Login işlemi
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = Student.query.filter_by(username=username).first()

    if not user:
        user = Teacher.query.filter_by(username=username).first()
    if not user:
        user = Admin.query.filter_by(username=username).first()

    if not user or not user.password == password:
        return jsonify({'error': 'Invalid credentials'}), 401

    access_token = create_access_token(identity=user.id)
    
    return jsonify({'access_token': access_token, 'role': user.role}), 200
