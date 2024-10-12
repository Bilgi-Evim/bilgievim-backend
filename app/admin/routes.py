from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Admin
from . import admin_bp
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import Teacher

# Admin Dashboard
@admin_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def admin_dashboard():
    user_id = get_jwt_identity()
    user = Admin.query.get(user_id)

    if user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403

    return jsonify({'message': 'Admin dashboard'}), 200

# Kullanıcı Listesini Getir (Admin için)
@admin_bp.route('/students', methods=['GET'])
@jwt_required()
def get_users():
    user_id = get_jwt_identity()
    user = Admin.query.get(user_id)

    if user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403

    # Tüm kullanıcıları listele
    users = Admin.query.all()
    users_list = [{"id": u.id, "username": u.username, "role": u.role} for u in users]

    return jsonify(users_list), 200

# Kullanıcı Sil (Admin için)
@admin_bp.route('/user/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    user_id_admin = get_jwt_identity()
    admin_user = Admin.query.get(user_id_admin)

    if admin_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403

    user_to_delete = Admin.query.get(user_id)
    if not user_to_delete:
        return jsonify({'error': 'User not found'}), 404

    # Kullanıcıyı sil
    db.session.delete(user_to_delete)
    db.session.commit()

    return jsonify({'message': 'User deleted successfully'}), 200

# Öğretmen kayıt işlemi
@admin_bp.route('/create-teacher', methods=['POST'])
@jwt_required()
def register_teacher():
    data = request.get_json()
    username = data.get('username')
    lastname = data.get('lastname')
    tc = data.get('tc')
    teacher_number = data.get('teacher_number')
    password = data.get('password')
    subject = data.get('subject')

    if Teacher.query.filter_by(tc=tc).first():
        return {"error": "Bu Tc kimlik numarasına sahip başka bir öğretmen var"}, 400
    if Teacher.query.filter_by(teacher_number=teacher_number).first():
        return {"error": "Bu numarada farklı bir öğretmen var"}, 400

    hashed_password = generate_password_hash(password)
    new_teacher = Teacher(username=username, lastname=lastname, tc=tc,
                          teacher_number=teacher_number, password=hashed_password,
                          role='teacher', subject=subject)

    db.session.add(new_teacher)
    db.session.commit()

    return {"message": "Teacher registered successfully"}, 201

# Öğretmen silme işlemi
@admin_bp.route("/delete-teacher/<int:teacher_id>",methods=['DELETE'])
@jwt_required()
def delete_teacher(teacher_id):
    user_id_admin = get_jwt_identity()
    admin_user = Admin.query.get(user_id_admin)

    if admin_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403

    teacher_to_delete = Teacher.query.get(teacher_id)
    if not teacher_to_delete:
        return jsonify({'error': 'Teacher not found'}), 404

    # Öğretmeni sil
    db.session.delete(teacher_to_delete)
    db.session.commit()

    return jsonify({'message': 'Teacher deleted successfully'}), 200