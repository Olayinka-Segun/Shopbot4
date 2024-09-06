from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db, login_manager
from sqlalchemy.orm import relationship
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to SearchHistory
    searches = db.relationship('SearchHistory', backref='user', lazy=True)

    # Method to set the password (hashes the password)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Method to check the password (compares the hashed password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class SearchHistory(db.Model):
    __tablename__ = 'search_history'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Fixed foreign key reference
    query = db.Column(db.String(255), nullable=False)
    search_time = db.Column(db.DateTime, default=datetime.utcnow)
    results = db.Column(db.JSON)  # Assuming JSON is required for results


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    price = db.Column(db.String(50))  # Ensure this field is in a consistent format
    link = db.Column(db.String(255))
    source = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    rating = db.Column(db.Float)  # Add rating attribute

