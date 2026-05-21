from flask import Flask

from app.config import Config
from app.api.routes import api_bp
from app.errors.handlers import register_error_handlers


def register_blueprints(app: Flask):
    app.register_blueprint(api_bp, url_prefix='/api/v1')

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    register_blueprints(app)
    register_error_handlers(app)
    
    return app
