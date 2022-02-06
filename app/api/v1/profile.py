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
