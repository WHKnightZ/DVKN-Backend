from functools import wraps

from flask import request
from flask_jwt_extended import (
    verify_jwt_in_request, get_jwt_claims
)

from app.api.helper import send_error
from app.enums import ADMIN_ROUTE


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

            if ADMIN_ROUTE in request.url_rule.rule:
                claims = get_jwt_claims()
                is_admin = claims.get("is_admin")
                if not is_admin:
                    return send_error(message='Bạn không có quyền truy cập')

            return fn(*args, **kwargs)

        return decorator

    return wrapper
