# Import necessary modules from Flask and other libraries
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

# Initialize SQLAlchemy and set the database name
db = SQLAlchemy()
DB_NAME = "database.db"  # Name of the database file

# Function to create the Flask application
def create_app():
    app = Flask(__name__)  # Initialize the Flask app
    app.config['SECRET_KEY'] = "helloworld"  # Secret key for session management
    # Configuring the database URI for PostgreSQL connection
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1catfish@localhost/blogApplication'

    # Initialize the SQLAlchemy extension with the Flask app
    db.init_app(app)

    # Import the views and auth modules (blueprints) for routing
    from .views import views
    from .auth import auth

    # Register blueprints with specific URL prefixes
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    # Import the models to ensure they are available for use
    from .models import User, Post, Comment, Like

    # Create the database tables if they don't already exist
    create_database(app)

    # Initialize the LoginManager for user authentication
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"  # Set the login view route
    login_manager.init_app(app)  # Initialize login manager with the app

    # Define a callback function to load the user based on user ID
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))  # Query user from the database by ID

    # Return the Flask app instance
    return app

# Function to create the database tables
def create_database(app):
    with app.app_context():  # Ensure app context is active
        db.create_all()  # Create all tables defined in the models
        print("Created tables in PostgreSQL!")  # Print confirmation message
