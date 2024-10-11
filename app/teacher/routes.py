from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Teacher
from . import teacher_bp

# Öğretmen Dashboard
@teacher_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def teacher_dashboard():
    user_id = get_jwt_identity()
    user = Teacher.query.get(user_id)
    
    if user.role != 'teacher':
        return jsonify({'error': 'Unauthorized'}), 403
    
    return jsonify({'message': 'Teacher dashboard'}), 200

# Öğretmen Profil Bilgilerini Getir
@teacher_bp.route('/profile', methods=['GET'])
@jwt_required()
def teacher_profile():
    user_id = get_jwt_identity()
    user = Teacher.query.get(user_id)

    if user.role != 'teacher':
        return jsonify({'error': 'Unauthorized'}), 403

    return jsonify({
        'username': user.username,
        'role': user.role
    }), 200

# Öğrenci Listesini Getir (Öğretmen için)
@teacher_bp.route('/students', methods=['GET'])
@jwt_required()
def get_students():
    user_id = get_jwt_identity()
    user = Teacher.query.get(user_id)

    if user.role != 'teacher':
        return jsonify({'error': 'Unauthorized'}), 403

    students = Teacher.query.filter_by(role='student').all()
    students_list = [{"id": student.id, "username": student.username} for student in students]

    return jsonify(students_list), 200
