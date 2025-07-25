# Add Datadog tracing at the top
from ddtrace import patch_all, tracer
patch_all()

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from .config import Config

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    jwt.init_app(app)

    from .routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    return app
