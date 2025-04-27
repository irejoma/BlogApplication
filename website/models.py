# Import necessary modules
from . import db  # Import the database instance
from flask_login import UserMixin  # Import UserMixin for Flask-Login integration
from sqlalchemy.sql import func  # Import function to handle automatic timestamps

# User model: Represents a user in the application
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each user
    email = db.Column(db.String(150), unique=True)  # User's email, must be unique
    username = db.Column(db.String(150), unique=True)  # User's username, must be unique
    password = db.Column(db.String(150))  # Store the password (plain text here, ideally should be hashed)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())  # Timestamp for when the user was created
    # Define relationships to other models (Post, Comment, Like)
    posts = db.relationship('Post', backref='user', passive_deletes=True)  # One-to-many relationship with posts
    comments = db.relationship('Comment', backref='user', passive_deletes=True)  # One-to-many relationship with comments
    likes = db.relationship('Like', backref='user', passive_deletes=True)  # One-to-many relationship with likes
    
    # Method to set password (stores plain text for now)
    def set_password(self, password):
        self.password = password  # Set the user's password (plain text)
    
    # Method to check password (compares plain text password)
    def check_password(self, password):
        return self.password == password  # Check if the provided password matches the stored one

# Post model: Represents a post created by a user
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each post
    text = db.Column(db.Text, nullable=False)  # Content of the post (cannot be null)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())  # Timestamp for when the post was created
    # Define relationship with User and other models
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)  # Foreign key to User model (author of the post)
    comments = db.relationship('Comment', backref='post', passive_deletes=True)  # One-to-many relationship with comments
    likes = db.relationship('Like', backref='post', passive_deletes=True)  # One-to-many relationship with likes

# Comment model: Represents a comment on a post
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each comment
    text = db.Column(db.String(200), nullable=False)  # Content of the comment (cannot be null)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())  # Timestamp for when the comment was created
    # Define relationships with User and Post models
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)  # Foreign key to User model (author of the comment)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete="CASCADE"), nullable=False)  # Foreign key to Post model (which post the comment belongs to)

# Like model: Represents a like on a post by a user
class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each like
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())  # Timestamp for when the like was created
    # Define relationships with User and Post models
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)  # Foreign key to User model (who liked the post)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete="CASCADE"), nullable=False)  # Foreign key to Post model (which post was liked)
