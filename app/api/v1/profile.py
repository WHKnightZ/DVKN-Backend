from flask import Blueprint
from app.api.functions import get_time_full_health

from app.api.helper import send_result
from app.gateway import authorization_require
from app.models import User
from app.validator import UserSchema

api = Blueprint('profile', __name__)


@api.route('', methods=['GET'])
@authorization_require()
def get_profile():
    current_user = User.get_current_user()
    dumped_user = UserSchema().dump(current_user)

    current_health, max_health, full_health_seconds, full_health_timestamp = get_time_full_health(current_user.username)
    dumped_user = {**dumped_user, "current_health": current_health,
                   "max_health": max_health, "full_health_seconds": full_health_seconds, "full_health_timestamp": full_health_timestamp}

    return send_result(data=dumped_user)
