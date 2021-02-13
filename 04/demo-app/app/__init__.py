from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects import mysql
from flask_migrate import Migrate

db = SQLAlchemy()


def create_app(app_config):
    app = Flask(__name__)
    app.config.from_object(app_config)
    db.init_app(app)

    migrate = Migrate(app, db)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app
