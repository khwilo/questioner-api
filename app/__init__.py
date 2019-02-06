'''Application entry module'''
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from flasgger import Swagger

from app.api.v2 import AUTH_BLUEPRINT, API_BLUEPRINT

from instance.config import APP_CONFIG

def create_app(config_name):
    '''Instantiate the Flask application'''
    app = Flask(__name__, instance_relative_config=True)
    jwt = JWTManager(app)
    CORS(app)

    app.config.from_object(APP_CONFIG[config_name])
    app.config.from_pyfile('config.py')
    app.config['SWAGGER'] = {'title': 'Questioner API', 'uiversion': 3}

    app.register_blueprint(AUTH_BLUEPRINT)
    app.register_blueprint(API_BLUEPRINT)

    template = {
        "swagger": "3.0",
        "info": {
            "title": "Questioner API",
            "description": "API documentation for the Questioner application",
            "version": "2.0.0"
        }
    }

    Swagger(app, template=template)

    return app
