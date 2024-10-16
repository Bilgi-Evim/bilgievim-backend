from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Admin
from . import admin_bp
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import Teacher,Admin,Student,Subject

# Admin Dashboard
@admin_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def admin_dashboard():
    user_id = get_jwt_identity()
    user = Admin.query.get(user_id)

    if user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403

    return jsonify({'message': 'Admin dashboard'}), 200

# Admin Bilgi Güncelleme
@admin_bp.route("/<int:admin_id>", methods=["PUT"])
@jwt_required()
def admin_update(admin_id):
    user_id = get_jwt_identity()
    admin = Admin.query.get(user_id)
    
    if admin.role != "admin":
        return jsonify({'error':'Unauthorized'}), 403

    data = request.get_json()
   
    admin.name = data.get('name', admin.name)
    admin.password = data.get('password', admin.password)
    
    if data.get('password'):
        admin.password = generate_password_hash(data['password'])

    db.session.commit()

    return jsonify({'message': 'Admin profile updated successfully', 'admin': {
        'id': admin.id,
        'name': admin.name,
        'role': admin.role
    }}), 200

# Tüm öğrencileri getir
@admin_bp.route("/student-list", methods=["GET"])
@jwt_required()
def get_students():
    user_id = get_jwt_identity()
    admin_user = Admin.query.get(user_id)
    
    if admin_user.role != "admin":
        return jsonify({'error':'Unauthorized'}), 403
    
    students = Student.query.all()
    student_list = [{"id": s.id, "name":s.name, "lastname":s.lastname, "school_number":s.school_number,"tc":s.tc, "grade":s.grade} for s in students]
    
    return jsonify(student_list), 200

# Öğrenci Profili Güncelleme
@admin_bp.route("/student/<int:student_id>",methods=["PUT"])
@jwt_required()
def update_student(student_id):
    user_id = get_jwt_identity()
    admin_user = Admin.query.get(user_id)
    
    if admin_user.role != "admin":
        return jsonify({'error': 'Unauthorized'}), 403

    student_to_upg = Student.query.get(student_id)
    if not student_to_upg:
        return jsonify({"error":"Student not found"}), 404 

    data = request.get_json()
    
    student_to_upg.name = data.get('name', student_to_upg.name)
    student_to_upg.lastname = data.get('lastname', student_to_upg.lastname)
    student_to_upg.tc = data.get('tc', student_to_upg.tc)
    student_to_upg.school_number = data.get('school_number', student_to_upg.school_number)
    student_to_upg.grade = data.get('grade', student_to_upg.grade)
    
    db.session.commit()
    
    return jsonify({'message': 'Student updated successfully', 'student': {
        'id': student_to_upg.id,
        'name': student_to_upg.name,
        'lastname': student_to_upg.lastname,
        'tc': student_to_upg.tc,
        'school_number': student_to_upg.school_number,
        'grade': student_to_upg.grade
    }}), 200


# Öğretmen Profili Güncelleme
@admin_bp.route("/teacher/<int:teacher_id>", methods=["PUT"])
@jwt_required()
def update_teacher(teacher_id):
    user_id = get_jwt_identity()
    admin_user = Admin.query.get(user_id)
    
    if admin_user.role != "admin":
        return jsonify({'error': 'Unauthorized'}), 403
    
    teacher = Teacher.query.get(teacher_id)
    if not teacher:
        return jsonify({"error":"Teacher not found"}), 404

    
    data = request.get_json()

    teacher.name = data.get('name', teacher.name)
    teacher.lastname = data.get('lastname', teacher.lastname)
    teacher.tc = data.get('tc', teacher.tc)
    teacher.teacher_number = data.get('teacher_number', teacher.teacher_number)
    teacher.subject = data.get('subject', teacher.subject)
    
    db.session.commit()

    return jsonify({'message': 'Teacher updated successfully', 'teacher': {
        'id': teacher.id,
        'name': teacher.name,
        'lastname': teacher.lastname,
        'tc': teacher.tc,
        'teacher_number': teacher.teacher_number,
        'subject': teacher.subject
    }}), 200


# Öğrenci Sil
@admin_bp.route('/student/<int:student_id>', methods=['DELETE'])
@jwt_required()
def delete_user(student_id):
    user_id_admin = get_jwt_identity()
    admin_user = Admin.query.get(user_id_admin)

    if admin_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403

    user_to_delete = Student.query.get(student_id)
    if not user_to_delete:
        return jsonify({'error': 'Student not found'}), 404

    # Kullanıcıyı sil
    db.session.delete(user_to_delete)
    db.session.commit()

    return jsonify({'message': 'User deleted successfully'}), 200

# Öğrenci Kayıt İşlemi    
@admin_bp.route('/create-student', methods=['POST'])
@jwt_required()
def register_student():
    user_id_admin = get_jwt_identity()
    admin_user = Admin.query.get(user_id_admin)

    if admin_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json()
    name = data.get('name')
    lastname = data.get('lastname')
    tc = data.get('tc')
    school_number = data.get('school_number')
    password = data.get('password')
    grade = data.get('grade', None)

    if Student.query.filter_by(tc=tc).first():
        return {"error": "Bu tc kimlik numarasına sahip bir öğrenci var"}, 400
    if Student.query.filter_by(school_number=school_number).first():
        return {"error": "Bu okul numarasına sahip bir kişi var"}, 400

    hashed_password = generate_password_hash(password)
    new_student = Student(name=name, lastname=lastname, tc=tc,
                          school_number=school_number, password=hashed_password,
                          role='student', grade=grade)
    
    db.session.add(new_student)
    db.session.commit()

    return {"message": "Student registered successfully"}, 201

# Öğretmen kayıt işlemi
@admin_bp.route('/create-teacher', methods=['POST'])
@jwt_required()
def register_teacher():
    data = request.get_json()
    name = data.get('name')
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
    new_teacher = Teacher(name=name, lastname=lastname, tc=tc,
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

# Öğretmen Kullanıcı Listesini Getir
@admin_bp.route('/teacher-list', methods=['GET'])
@jwt_required()
def get_teachers():
    user_id = get_jwt_identity()
    admin_user = Admin.query.get(user_id)

    # Admin kontrolü
    if admin_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403

    # Tüm öğretmenleri listele
    teachers = Teacher.query.all()
    teachers_list = [{"id": t.id, "name": t.name, "lastname": t.lastname, 
                      "tc": t.tc, "teacher_number": t.teacher_number, "subject": t.subject} 
                     for t in teachers]

    return jsonify(teachers_list), 200


@admin_bp.route("/add-subject", methods=["POST"])
@jwt_required()
def add_subject():
    user_id = get_jwt_identity()
    admin = Admin.query.get(user_id)
    
    if admin.role != "admin":
        return jsonify({"error":"Unauthorized"}), 403
    
    data = request.get_json()
    subject_name = data.get("subject_name")
    subject_code = data.get("subject_code")
    
    if Subject.query.filter_by(subject_name = subject_name).first():
        return {"error":"Bu ders adına sahip başka bir ders var"}
    
    if Subject.query.filter_by(subject_code = subject_code).first():
        return {"error":"Bu ders koduna sahip başka bir ders var"}
    
    new_subject = Subject(subject_name = subject_name, subject_code = subject_code)
    
    db.session.add(new_subject)
    db.session.commit()
    
    return {"message": "Subject successfully added"}, 201
    