# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.DevelopmentConfig')
    
    db.init_app(app)
    jwt = JWTManager(app)
    
    CORS(app)
    
    from .auth.routes import auth_bp
    from .teacher.routes import teacher_bp
    from .student.routes import student_bp 
    from .admin.routes import admin_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(teacher_bp, url_prefix='/teacher')
    app.register_blueprint(student_bp, url_prefix='/student')  # Burada kayıt ediyoruz
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    return app
