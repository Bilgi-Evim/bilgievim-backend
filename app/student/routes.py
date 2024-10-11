from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User
from . import student_bp

@student_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def student_dashboard():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if user.role != 'student':
        return jsonify({'error': 'Unauthorized'}), 403
    
    return jsonify({'message': 'Student dashboard'}), 200

@student_bp.route('/profile', methods=['GET'])
@jwt_required()
def student_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if user.role != 'student':
        return jsonify({'error': 'Unauthorized'}), 403

    return jsonify({
        'username': user.username,
        'role': user.role
    }), 200
