from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

jwt = JWTManager()

# init SQLAlchemy
db = SQLAlchemy()
