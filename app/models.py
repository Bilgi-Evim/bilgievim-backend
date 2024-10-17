from app import db

class Class(db.Model):
    __tablename__ = 'class'
    id = db.Column(db.Integer, primary_key=True)
    grade = db.Column(db.String(10))
    students = db.relationship('Student', backref='class_', lazy=True)
    teachers = db.relationship('Teacher', backref='class_', lazy=True)

class Subject(db.Model):
    __tablename__ = 'subject'
    subject_id = db.Column(db.Integer, primary_key=True)
    subject_name = db.Column(db.String(100))
    subject_code = db.Column(db.String(5), unique=True, nullable=False)
    teachers = db.relationship('Teacher', backref='subject', lazy=True)
    private_lessons = db.relationship('PrivateLesson', backref='subject_info', lazy=True)

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    tc = db.Column(db.String(11), unique=True)
    school_number = db.Column(db.String(20), unique=True)
    role = db.Column(db.String(50))
    password = db.Column(db.String(100))
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'))
    private_lessons = db.relationship('PrivateLesson', backref='student_info', lazy=True)

class Teacher(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    tc = db.Column(db.String(11), unique=True)
    teacher_number = db.Column(db.String(20), unique=True)
    role = db.Column(db.String(50))
    password = db.Column(db.String(100))
    classroom_id = db.Column(db.Integer, db.ForeignKey('class.id'))
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.subject_id'))
    private_lessons = db.relationship('PrivateLesson', backref='taught_by', lazy=True, overlaps="private_lessons_taught")

class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    role = db.Column(db.String(50))
    password = db.Column(db.String(100))

class PrivateLesson(db.Model):
    __tablename__ = 'privatelesson'
    private_lesson_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.subject_id'))
    time = db.Column(db.DateTime)
    location = db.Column(db.String(255))
    
    student = db.relationship('Student', backref='lessons')
    subject = db.relationship('Subject', backref='lessons')
    teacher = db.relationship('Teacher', backref='private_lessons_taught', lazy=True, overlaps="private_lessons")
