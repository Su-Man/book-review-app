import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "devkey"
    SQLALCHEMY_DATABASE_URI = "sqlite:///bookreview.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY") or "jwt-secret-key"
