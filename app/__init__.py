'''Application entry module'''
from flask import Flask
from flask_jwt_extended import JWTManager

from app.api.v1 import AUTH_BLUEPRINT, API_BLUEPRINT
from app.api.v2 import API_V2_BLUEPRINT

from instance.config import APP_CONFIG

def create_app(config_name):
    '''Instantiate the Flask application'''
    app = Flask(__name__, instance_relative_config=True)
    jwt = JWTManager(app)

    app.config.from_object(APP_CONFIG[config_name])
    app.config.from_pyfile('config.py')

    app.register_blueprint(AUTH_BLUEPRINT)
    app.register_blueprint(API_BLUEPRINT)

    app.register_blueprint(API_V2_BLUEPRINT)

    return app
