# Import necessary modules from Flask and other libraries
from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db  # Import the database instance
from .models import User  # Import the User model
from flask_login import login_user, logout_user, login_required, current_user  # Import login-related functions
from werkzeug.security import generate_password_hash, check_password_hash  # Import functions for password hashing

# Create a Blueprint for the authentication routes
auth = Blueprint("auth", __name__)

# Login route: Handles both GET and POST requests for user login
@auth.route("/login", methods=['GET', 'POST'])
def login():
    # If the method is POST, attempt to log in the user
    if request.method == 'POST':
        email = request.form.get("email")  # Get email from the form
        password = request.form.get("password")  # Get password from the form

        # Fetch the user from the database using the provided email
        user = User.query.filter_by(email=email).first()
        if user:
            # Check if the provided password matches the stored password hash
            if check_password_hash(user.password, password):
                flash("Logged in!", category='success')  # Flash success message
                login_user(user, remember=True)  # Log the user in and remember the session
                return redirect(url_for('views.home'))  # Redirect to home page
            else:
                flash('Password is incorrect.', category='error')  # Flash error message for incorrect password
        else:
            flash('Email does not exist.', category='error')  # Flash error message for non-existent email

    return render_template("login.html", user=current_user)  # Render the login template with current user info


# Sign-up route: Handles both GET and POST requests for user registration
@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    # If the method is POST, attempt to register the user
    if request.method == 'POST':
        email = request.form.get("email")  # Get email from the form
        username = request.form.get("username")  # Get username from the form
        password1 = request.form.get("password1")  # Get the first password input
        password2 = request.form.get("password2")  # Get the second password input for confirmation

        # Check if the email or username already exists in the database
        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()

        if email_exists:
            flash('Email is already in use.', category='error')  # Flash error message if email exists
        elif username_exists:
            flash('Username is already in use.', category='error')  # Flash error message if username exists
        elif password1 != password2:
            flash('Passwords don\'t match!', category='error')  # Flash error if passwords don't match
        elif len(username) < 2:
            flash('Username is too short.', category='error')  # Flash error if username is too short
        elif len(password1) < 6:
            flash('Password is too short.', category='error')  # Flash error if password is too short
        elif len(email) < 4:
            flash("Email is invalid.", category='error')  # Flash error if email is invalid
        else:
            # Create a new user with the hashed password
            hashed_password = generate_password_hash(password1, method='pbkdf2:sha256')  # Hash the password
            new_user = User(email=email, username=username, password=hashed_password)  # Create user instance
            db.session.add(new_user)  # Add user to the session
            db.session.commit()  # Commit the transaction to save the user to the database
            login_user(new_user, remember=True)  # Log the new user in automatically
            flash('User created!', category='success')  # Flash success message
            return redirect(url_for('views.home'))  # Redirect to home page

    return render_template("signup.html", user=current_user)  # Render the sign-up template with current user info


# Logout route: Logs out the current user and redirects to home page
@auth.route("/logout")
@login_required  # Ensure that only authenticated users can access this route
def logout():
    logout_user()  # Log the user out
    return redirect(url_for("views.home"))  # Redirect to home page
