from flask import Flask

from .config import Config
from .api.routes import api_bp
from .errors.handlers import register_error_handlers


def register_blueprints(app: Flask):
    app.register_blueprint(api_bp, url_prefix="/api/v1")


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    register_blueprints(app)
    register_error_handlers(app)

    return app
