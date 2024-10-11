from app import db

class Student(db.Model):
    __tablename__ = 'students' 
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    tc = db.Column(db.String(11), unique=True, nullable=False)
    school_number = db.Column(db.String(5), unique = True, nullable = False)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(7), nullable=False)  
    grade = db.Column(db.String(10), nullable=True) 
    

class Teacher(db.Model):
    __tablename__ = 'teachers'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    tc = db.Column(db.String(11), unique=True, nullable=False)
    teacher_number = db.Column(db.String(5), unique = True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(7), nullable=False) 
    subject = db.Column(db.String(100), nullable=False)
    

class Admin(db.Model):
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(7), nullable=False)  
