from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from dotenv import load_dotenv
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    load_dotenv()
    
    app.config.from_object('app.config.DevelopmentConfig')
    
    db.init_app(app)
    jwt = JWTManager(app)
    
    cors_origin = os.getenv('CORS_ORIGIN')
    CORS(app, resources={r"/*": {"origins": cors_origin}})
    
    SWAGGER_URL = '/swagger'  
    API_URL = '/static/swagger.json' 
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={  
            'app_name': "Bilgi Evim API"
        }
    )
    # Blueprint kayıtları
    from .auth.routes import auth_bp
    from .teacher.routes import teacher_bp
    from .student.routes import student_bp
    from .admin.routes import admin_bp 

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(teacher_bp, url_prefix='/teacher')
    app.register_blueprint(student_bp, url_prefix='/student')
    app.register_blueprint(admin_bp, url_prefix='/admin') 
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
    
    return app
