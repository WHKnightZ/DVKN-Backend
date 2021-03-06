from functools import wraps

from flask import request
from flask_jwt_extended import (
    verify_jwt_in_request, get_jwt_claims, get_jwt_identity
)
from app.api.functions import update_user_health

from app.api.helper import send_error
from app.enums import ADMIN_ROUTE, MSG_AUTH_ERROR


def authorization_require():
    """
    validate authorization follow permission user
    Args:

    Returns:

    """

    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            username = get_jwt_identity()
            update_user_health(username)

            if ADMIN_ROUTE in request.url_rule.rule:
                claims = get_jwt_claims()
                is_admin = claims.get("is_admin")
                if not is_admin:
                    return send_error(message_id=MSG_AUTH_ERROR)

            return fn(*args, **kwargs)

        return decorator

    return wrapper
