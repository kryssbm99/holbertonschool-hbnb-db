""" Initialize the Flask app. """

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from src.config import DevelopmentConfig, TestingConfig, ProductionConfig
from src.models.user import User
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()

cors = CORS()


def create_app(config_class):
    """
    Create a Flask app with the given configuration class.
    The default configuration class is DevelopmentConfig.
    """
    app = Flask(__name__)

    if config_class == "Development":
        app.config.from_object(DevelopmentConfig)
    elif config_class == "Testing":
        app.config.from_object(TestingConfig)
    elif config_class == "Production":
        app.config.from_object(ProductionConfig)
    else:
        raise ValueError("Invalid configuration name")

    print("Using configuration:", config_class)
    print("Database URI:", app.config['SQLALCHEMY_DATABASE_URI'])

    app.config['SQLALCHEMY_ECHO'] = True

    # Initialize app with database
    db.init_app(app)
    Migrate(app, db)
    
    # Setup JWT
    jwt = JWTManager(app)

    # Register blueprints
    from src.routes.security import security_bp
    app.register_blueprint(security_bp, url_prefix='/')

   
    with app.app_context():
        if config_class == "Testing":
            db.create_all()
            test_user = User(email='Juan123@example.com', is_admin=True)
            test_user.set_password('passcode123')
            db.session.add(test_user)
            db.session.commit()

    return app
