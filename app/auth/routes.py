from flask import jsonify, request
from flask_jwt_extended import create_access_token
from app.models import Teacher, Student, Admin
from . import auth_bp
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

# Öğrenci Giriş işlemi
@auth_bp.route('/login/student', methods=['POST'])
def studentLogin():
    data = request.get_json()
    tc = data.get('tc')
    school_number = data.get('school_number')
    password = data.get('password')

    user = Student.query.filter_by(tc=tc).first()

    if not user or not user.password == password or not user.school_number == school_number:
        return jsonify({'error': 'Invalid credentials'}), 401

    access_token = create_access_token(identity=user.id)
    
    return jsonify({'access_token': access_token, 'role': user.role}), 200

# Öğrenci Kayıt İşlemi    
@auth_bp.route('/register/student', methods=['POST'])
def register_student():
    data = request.get_json()
    username = data.get('username')
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
    new_student = Student(username=username, lastname=lastname, tc=tc,
                          school_number=school_number, password=hashed_password,
                          role='student', grade=grade)
    
    db.session.add(new_student)
    db.session.commit()

    return {"message": "Student registered successfully"}, 201



# Öğretmen giriş işlemi
@auth_bp.route('/login/teacher', methods=['POST'])
def login_teacher():
    data = request.get_json()
    tc = data.get('tc')
    password = data.get('password')

    teacher = Teacher.query.filter_by(tc=tc).first()
    if not teacher or not check_password_hash(teacher.password, password):
        return {"error": "Invalid credentials"}, 401

    return {"message": "Login successful", "username": teacher.username}, 200


# Admin Giriş
@auth_bp.route('/login/admin', methods=['POST'])
def login_admin():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    admin = Admin.query.filter_by(username=username).first()
    if not admin or not check_password_hash(admin.password, password):
        return {"error": "Invalid credentials"}, 401

    return {"message": "Login successful", "username": admin.username}, 200