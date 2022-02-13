from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import logging
import os

jwt = JWTManager()

# init SQLAlchemy
db = SQLAlchemy()

if os.environ.get('ENV') == 'prd':
    log = logging.getLogger('werkzeug')
    log.disabled = True
