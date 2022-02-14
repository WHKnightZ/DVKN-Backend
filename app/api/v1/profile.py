from flask import Blueprint

from app.api.helper import send_result
from app.gateway import authorization_require
from app.models import User
from app.validator import UserSchema

api = Blueprint('profile', __name__)


@api.route('', methods=['GET'])
@authorization_require()
def get_profile():
    current_user = User.get_current_user()

    return send_result(data=UserSchema().dump(current_user))
