import wtforms_json
from flask import Flask

from app.helpers import db
from app.routes.endpoints import v1
from app.routes.errors import register_error_handlers
from config import load_config


def create_app():
    """Initialize the core application."""
    app = Flask(__name__)
    app.config.from_object(load_config())

    # Initialize Plugins
    db.init_app(app)
    wtforms_json.init()

    # Blueprint Register
    app.register_blueprint(v1, url_prefix='/v1')

    # init error handlers
    register_error_handlers(app)
    return app
