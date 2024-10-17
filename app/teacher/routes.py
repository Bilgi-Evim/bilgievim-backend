from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Teacher, PrivateLesson
from . import teacher_bp
from app import db


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

@teacher_bp.route("/create-private-lesson", methods=["POST"])
@jwt_required()
def create_private_lesson():
    user_id = get_jwt_identity()
    user = Teacher.query.get(user_id)
    
    if user.role != "teacher":
        return jsonify({"error": "Unauthorized"}), 403
    
    data = request.get_json()
    description = data.get("description")
    time = data.get("time")
    student_id = data.get("student_id")
    subject_id = data.get("subject_id")
    location = data.get("location")
    
    new_private_lesson = PrivateLesson(description=description, time=time,student_id=student_id, teacher_id=user_id,subject_id=subject_id,location=location)
    
    db.session.add(new_private_lesson)
    db.session.commit()
    
    return{"message": "Private lesson successfully added"}, 201
    
    
@teacher_bp.route("/private-lessons", methods=["GET"])
@jwt_required()
def list_private_lessons():
    user_id = get_jwt_identity()
    user = Teacher.query.get(user_id)
    
    if user.role != "teacher":
        return jsonify({"error": "Unauthorized"}), 403
    
    
    lessons = PrivateLesson.query.filter_by(teacher_id = user_id).all()
    lesson_list = [{"id": lesson.private_lesson_id, "student_id": lesson.student_id, "ders":lesson.subject_id, "time":lesson.time, "location":lesson.location} for lesson in lessons]

    return jsonify(lesson_list), 200