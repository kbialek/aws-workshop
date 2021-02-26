import os

from app import create_app

config_name = os.getenv('FLASK_CONFIG')
from config import app_config

app = create_app(app_config[config_name])


if __name__ == '__main__':
    app.run()
