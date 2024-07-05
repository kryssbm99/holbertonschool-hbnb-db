import os
import logging
from flask import Flask, jsonify, request
from flask_swagger_ui import get_swaggerui_blueprint
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from dotenv import load_dotenv
from src import db
from src.config import get_config

# Import models
from src.models.user import User
from src.models.amenity import Amenity
from src.models.place import Place
from src.models.country import Country
from src.models.review import Review
from src.models.city import City

# Import route blueprints
from src.routes import users
from src.routes import countries
from src.routes import places
from src.routes import amenities
from src.routes import reviews
from src.routes import cities
from src.routes import security

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Load configuration from config file
app.config.from_object(get_config())

# Set up JWT manager
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this to a more secure key
jwt = JWTManager(app)

# Initialize the database with the app
db.init_app(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Swagger UI configuration
SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Test application"
    },
)

# Register blueprints for different routes
app.register_blueprint(swaggerui_blueprint)
app.register_blueprint(users)
app.register_blueprint(countries)
app.register_blueprint(places)
app.register_blueprint(amenities)
app.register_blueprint(reviews)
app.register_blueprint(cities)
app.register_blueprint(security)

if __name__ == "__main__":
    with app.app_context():
        logging.debug("Creating database tables...")

        # Create database tables
        db.create_all()

        logging.debug("Tables created.")

    # Start the app on the specified port (default: 5002)
    port = os.getenv("PORT", 5002)
    logging.debug(f"Starting app on port {port}")
    app.run(debug=True, host='0.0.0.0', port=port)
