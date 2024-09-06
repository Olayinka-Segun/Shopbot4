from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from extensions import db
from auth.models import User
from auth.forms import RegistrationForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash

# Define Blueprint for authentication routes
auth_bp = Blueprint('auth_bp', __name__)

# Helper function to hash password
def hash_password(password):
    return generate_password_hash(password)

# Helper function to check hashed password
def verify_password(password, hashed_password):
    return check_password_hash(hashed_password, password)

@auth_bp.route('/')
def base():
    return render_template('base.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('auth_bp.chat'))

    form = RegistrationForm(request.form)
    
    if request.method == 'POST' and form.validate():
        # Check if the user already exists
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('Email is already registered', 'danger')
            return redirect(url_for('auth_bp.register'))

        # Hash the password and create a new user
        hashed_password = hash_password(form.password.data)
        new_user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password)

        # Add the user to the database
        db.session.add(new_user)
        db.session.commit()

        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('auth_bp.login'))

    return render_template('base.html', form=form, action='register')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth_bp.chat'))

    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()

        if user and verify_password(form.password.data, user.password_hash):
            login_user(user)
            flash('You have been logged in!', 'success')
            return redirect(url_for('auth_bp.chat'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')

    return render_template('base.html', form=form, action='login')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth_bp.login'))

@auth_bp.route('/chat')
@login_required
def chat():
    return render_template('chat.html')
