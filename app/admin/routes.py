from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Admin
from . import admin_bp
from app import db

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
@admin_bp.route('/users', methods=['GET'])
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
