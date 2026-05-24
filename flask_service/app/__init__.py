from flask import Flask

from .config import Config
from .api.routes import api_bp
from .errors.handlers import register_error_handlers
from .extensions import db, migrate


def register_blueprints(app: Flask):
    app.register_blueprint(api_bp, url_prefix="/api/v1")

def register_extensions(app: Flask):
    db.init_app(app)
    migrate.init_app(app, db)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    register_extensions(app)

    from app.models import Review

    register_blueprints(app)
    register_error_handlers(app)

    return app
