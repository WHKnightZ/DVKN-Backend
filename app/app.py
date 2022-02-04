# -*- coding: utf-8 -*-

from flask import Flask
from flask_cors import CORS

from app.api.helper import CONFIG
from app.extensions import jwt, db
from .api import v1 as api_v1
from .api.helper import send_error


def create_app(config_object=CONFIG):
    """
    Init App
    :param config_object:
    :return:
    """
    app = Flask(__name__, static_url_path="", static_folder="./files")
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    CORS(app)

    return app


def register_extensions(app):
    """
    Init extension
    :param app:
    :return:
    """

    db.app = app
    db.init_app(app)  # SQLAlchemy
    jwt.init_app(app)

    @app.after_request
    def after_request(response):
        """

        :param response:
        :return:
        """
        return response

    @app.errorhandler(Exception)
    def exceptions(e):
        """
        Handling exceptions
        :param e:
        :return:
        """
        code = 500
        if hasattr(e, 'code'):
            code = e.code

        return send_error(message=str(e), code=code)


def register_blueprints(app):
    """
    Init blueprint for api url
    :param app:
    :return:
    """
    app.register_blueprint(api_v1.manage.user.api,
                           url_prefix='/api/v1/manage/users')
    app.register_blueprint(api_v1.manage.card.api,
                           url_prefix='/api/v1/manage/cards')

    app.register_blueprint(api_v1.upload_file.api, url_prefix='/api/v1/upload')
    app.register_blueprint(api_v1.auth.api, url_prefix='/api/v1/auth')
    app.register_blueprint(api_v1.user.api, url_prefix='/api/v1/users')
    app.register_blueprint(api_v1.battle.api, url_prefix='/api/v1/battle')
