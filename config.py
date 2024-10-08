import os

from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Turn off Flask-SQLAlchemy modification tracking
    DEBUG = True
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    