import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:sege d boy@localhost/product_search_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
