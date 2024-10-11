from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Student
from . import student_bp

# Öğrenci dashboard'u
@student_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def student_dashboard():
    user_id = get_jwt_identity()  # JWT'den kullanıcı ID'sini alıyoruz
    user = Student.query.get(user_id)  # Veritabanından öğrenci bilgilerini alıyoruz

    # Rol kontrolü
    if not user or user.role != 'student':
        return jsonify({'error': 'Unauthorized'}), 403

    return jsonify({'message': 'Student dashboard'}), 200


# Öğrenci profil bilgilerini getirir
@student_bp.route('/profile', methods=['GET'])
@jwt_required()
def student_profile():
    user_id = get_jwt_identity()  # JWT'den kullanıcı ID'sini alıyoruz
    user = Student.query.get(user_id)  # Veritabanından öğrenci bilgilerini alıyoruz

    # Rol kontrolü
    if not user or user.role != 'student':
        return jsonify({'error': 'Unauthorized'}), 403

    return jsonify({
        'username': user.username,
        'role': user.role,
        'grade': user.grade  # Öğrencinin sınıfını da döndürelim
    }), 200
