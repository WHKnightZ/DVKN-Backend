import uuid

from flask import Blueprint, request
from werkzeug.security import check_password_hash, generate_password_hash

from app.api.helper import send_error, send_result
from app.extensions import db
from app.models import User
from app.utils import is_contain_space, get_timestamp_now
from app.validator import CreateUserValidation, UserSchema, ChangePasswordValidation
from app.gateway import authorization_require

api = Blueprint('manage/users', __name__)


@api.route('', methods=['POST'])
@authorization_require()
def create_user():
    """ This is api for the user management registers user admin. """

    try:
        json_req = request.get_json()
    except Exception as ex:
        return send_error(message="Request Body incorrect json format: " + str(ex), code=442)

    if json_req is None:
        return send_error(message='Please check your json requests', code=442)

    # trim input body
    json_body = {}
    for key, value in json_req.items():
        if isinstance(value, str):
            json_body.setdefault(key, value.strip())
        else:
            json_body.setdefault(key, value)

    # validate request body
    validator_input = CreateUserValidation()
    is_not_validate = validator_input.validate(json_body)
    if is_not_validate:
        return send_error(data=is_not_validate, message_id='11')

    username = json_body.get("username")
    password = json_body.get("password")

    duplicated_user = User.query.filter_by(username=username).first()
    if duplicated_user:
        return send_error(message="Tai khoan da ton tai")

    created_date = get_timestamp_now()
    _id = str(uuid.uuid1())

    new_user = User(id=_id, username=username, password_hash=generate_password_hash(password),
                    created_date=created_date, is_admin=True, avatar="")
    db.session.add(new_user)
    db.session.commit()

    return send_result(data=UserSchema().dump(new_user))


@api.route('/<user_id>', methods=['PUT'])
@authorization_require()
def update_user_admin(user_id):
    """ This is api for the user management edit the user admin.

        Request Body:

        Returns:

        Examples::

    """

    user = User.query.filter_by(id=user_id, type=2).first()
    if user is None:
        return send_error(message="Ko ton tai")

    try:
        json_req = request.get_json()
    except Exception as ex:
        return send_error(message="Request Body incorrect json format: " + str(ex), code=442)

    if json_req is None:
        return send_error(message='Please check your json requests', code=442)

    # trim input body
    json_body = {}
    for key, value in json_req.items():
        if isinstance(value, str):
            json_body.setdefault(key, value.strip())
        else:
            json_body.setdefault(key, value)

    # validate request body
    validator_input = CreateUserValidation()
    is_not_validate = validator_input.validate(json_body)
    if is_not_validate:
        return send_error(data=is_not_validate, message_id='11')

    full_name = json_body.get("full_name")
    permission_group_id = json_body.get("permission_group_id")
    is_active: bool = json_body.get("is_active", False)

    is_clear = False
    #  change permission group
    user.full_name = full_name
    if user.group_id != permission_group_id:
        is_clear = True
        user.group_id = permission_group_id

    user.modified_date = get_timestamp_now()
    db.session.commit()

    return send_result(data=UserSchema().dump(user))


@api.route('/profile', methods=['PUT'])
@authorization_require()
def update_info():
    """ This is api for all user edit their profile.

        Request Body:

        Returns:


        Examples::

    """

    current_user: User = User.get_current_user()
    if current_user is None:
        return send_error()

    try:
        json_req = request.get_json()
    except Exception as ex:
        return send_error(message="Request Body incorrect json format: " + str(ex), code=442)

    # validate request body
    validator_input = CreateUserValidation()
    is_not_validate = validator_input.validate(json_req)
    if is_not_validate:
        return send_error(data=is_not_validate)

    # update user info
    for key, value in json_req.items():
        setattr(current_user, key, value)

    current_user.modified_date = get_timestamp_now()
    db.session.commit()

    return send_result(data=UserSchema().dump(current_user))


@api.route('/password', methods=['PUT'])
@authorization_require()
def change_password():
    """ This api for all user change their password.

        Request Body:

        Returns:

        Examples::

    """

    current_user = User.get_current_user()

    try:
        json_req = request.get_json()
    except Exception as ex:
        return send_error(message="Request Body incorrect json format: " + str(ex), code=442)

    # validate request body
    validator_input = ChangePasswordValidation()
    is_not_validate = validator_input.validate(json_req)
    if is_not_validate:
        return send_error(data=is_not_validate, message_id="INVALID_PASSWORD")

    current_password = json_req.get("current_password")
    new_password = json_req.get("new_password")

    if not check_password_hash(current_user.password_hash, current_password):
        return send_error(message_id="INCORRECT_PASSWORD")

    if is_contain_space(new_password):
        return send_error(message_id="INVALID_PASSWORD")

    if new_password == current_password:
        return send_error(message_id="SAME_CURRENT_PASSWORD")

    current_user.password_hash = generate_password_hash(new_password)
    current_user.modified_date_password = get_timestamp_now()
    db.session.commit()

    data = {
        "new_password": new_password,
        "current_password": current_password
    }

    return send_result(data=data, message_id="CHANGE_PASSWORD_SUCCESS")


@api.route('/<user_id>', methods=['DELETE'])
@authorization_require()
def delete_user_admin(user_id):
    """ This api for the user management deletes the users.

        Returns:

        Examples::

    """
    user = User.get_by_id(user_id)
    if not user:
        return send_error(message_id="USER_NOT_EXISTED")

    db.session.delete(user)
    db.session.commit()

    return send_result(message_id="DELETED_SUCCESS")


@api.route('/<user_id>', methods=['GET'])
@authorization_require()
def get_user_by_id(user_id):
    """ This api get information of a user.

        Returns:

        Examples::

    """

    user = User.get_by_id(user_id)
    if user:
        user = UserSchema().dump(user)
    return send_result(data=user)


@api.route('/profile', methods=['GET'])
@authorization_require()
def get_profile():
    """ This api for the user get their information.

        Returns:

        Examples::

    """

    current_user = User.get_current_user()
    if current_user:
        current_user = UserSchema().dump(current_user)
    return send_result(data=current_user)
