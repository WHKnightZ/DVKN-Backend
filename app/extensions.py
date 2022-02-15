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

# Lưu sức khỏe của user với key là username, nếu key rỗng nghĩa là sức khỏe full
# user_healths = {
#     khanh.nguyen: (health, max_health, last_time)
# }
user_healths = {}
