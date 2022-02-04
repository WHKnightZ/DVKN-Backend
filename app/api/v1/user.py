from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity
from sqlalchemy import func

from app.api.helper import get_card_link, send_result
from app.extensions import db
from app.gateway import authorization_require
from app.models import User, UserCard

api = Blueprint('users', __name__)


@api.route('', methods=['GET'])
@authorization_require()
def get_all_users():
    username = get_jwt_identity()

    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)
    keyword = request.args.get('keyword', "", type=str)
    keyword = f"%{keyword}%"

    all_items = User.query.filter((User.username.like(keyword)), User.is_admin == 0)
    total = all_items.count()

    items = db.session.query(User.username, UserCard.card_id, UserCard.rank).join(UserCard, func.substring(
        User.deck, 1, 36) == UserCard.id).filter((User.username.like(keyword)), User.is_admin == 0, User.username != username)\
        .order_by(User.created_date.desc()).paginate(page=page, per_page=page_size,
                                                     error_out=False).items

    results = {
        "items": [{"username": item.username, "avatar": get_card_link(item.card_id, item.rank)} for item in items],
        "total": total,
    }

    return send_result(data=results)

# @api.route('/profile', methods=['PUT'])
# @authorization_require()
# def update_info():
#     """ This is api for all user edit their profile.

#         Request Body:

#         Returns:


#         Examples::

#     """

#     current_user = User.get_current_user()
#     if current_user is None:
#         return send_error(message="Not found user!")

#     try:
#         json_req = request.get_json()
#     except Exception as ex:
#         return send_error(message="Request Body incorrect json format: " + str(ex), code=442)

#     if json_req is None:
#         return send_error(message='Please check your json requests', code=442)

#     # trim input body
#     json_body = {}
#     for key, value in json_req.items():
#         if isinstance(value, str):
#             json_body.setdefault(key, value.strip())
#         else:
#             json_body.setdefault(key, value)

#     # validate request body
#     validator_input = AuthValidation()
#     is_not_validate = validator_input.validate(json_body)
#     if is_not_validate:
#         return send_error(data=is_not_validate, message_id="INVALID_PARAMETERS_ERROR")

#     for key, value in json_body.items():
#         if key == "date_of_birth":
#             # setattr(current_user, "date_of_birth_timestamp", date_of_birth_timestamp)
#             date_time_str = f"{value}"
#             date_time_obj = datetime.strptime(date_time_str, "FORMAT_DATE").date()
#             setattr(current_user, "birthday", date_time_obj)
#         setattr(current_user, key, value)

#     current_user.modified_date = get_timestamp_now()
#     db.session.commit()

#     return send_result(data=UserSchema().dump(current_user), message_id=CHANGE_PROFILE_SUCCESSFULLY)


# @api.route('/password', methods=['PUT'])
# @authorization_require()
# def change_password():
#     """ This api for all user change their password.

#         Request Body:

#         Returns:

#         Examples::

#     """

#     current_user = User.get_current_user()

#     try:
#         json_req = request.get_json()
#     except Exception as ex:
#         return send_error(message="Request Body incorrect json format: " + str(ex), code=442)

#     if json_req is None:
#         return send_error(message='Please check your json requests', code=442)

#     # trim input body
#     json_body = {}
#     for key, value in json_req.items():
#         if isinstance(value, str):
#             json_body.setdefault(key, value.strip())
#         else:
#             json_body.setdefault(key, value)

#     # validate request body
#     validator_input = ChangePasswordValidation()
#     is_not_validate = validator_input.validate(json_body)
#     if is_not_validate:
#         return send_error(data=is_not_validate, message_id=PASSWORD_INVALID)

#     current_password = json_body.get("current_password")
#     new_password = json_body.get("new_password")
#     if not check_password_hash(current_user.password_hash, current_password):
#         return send_error(message_id=CURRENT_PASSWORD_INCORRECT)

#     if new_password == current_password:
#         return send_error(message_id=NEW_PASSWORD_SAME_CURRENT_PASSWORD)

#     if is_contain_space(new_password):
#         return send_error(message_id=PASSWORD_INVALID)

#     current_user.password_hash = generate_password_hash(new_password)
#     current_user.modified_date_password = get_timestamp_now()
#     db.session.commit()

#     data = {
#         "new_password": new_password,
#         "current_password": current_password
#     }

#     return send_result(data=data, message_id=CHANGE_PASSWORD_SUCCESSFULLY)


# @api.route('/profile', methods=['GET'])
# @authorization_require()
# def get_profile():
#     """ This api for the user get their information.

#         Returns:

#         Examples::

#     """

#     current_user = User.get_current_user()

#     return send_result(data=UserSchema().dump(current_user))
