import uuid

from flask import Blueprint, request
from werkzeug.security import generate_password_hash

from app.api.helper import get_json_body, send_error, send_result
from app.extensions import db
from app.models import Card, User, UserCard
from app.utils import get_timestamp_now
from app.validator import AddUserCardValidation, UserSchema
from app.gateway import authorization_require

api = Blueprint('manage/users', __name__)


# @api.route('', methods=['POST'])
# @authorization_require()
# def create_user():
#     """ This is api for the user management registers user admin. """

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
#     validator_input = CreateUserValidation()
#     is_not_validate = validator_input.validate(json_body)
#     if is_not_validate:
#         return send_error(data=is_not_validate, message_id='11')

#     username = json_body.get("username")
#     password = json_body.get("password")

#     duplicated_user = User.query.filter_by(username=username).first()
#     if duplicated_user:
#         return send_error(message="Tai khoan da ton tai")

#     created_date = get_timestamp_now()
#     _id = str(uuid.uuid1())

#     new_user = User(id=_id, username=username, password_hash=generate_password_hash(password),
#                     created_date=created_date, is_admin=True, avatar="")
#     db.session.add(new_user)
#     db.session.commit()

#     return send_result(data=UserSchema().dump(new_user))


@api.route('', methods=['GET'])
@authorization_require()
def get_all_users():
    params = request.args

    page = params.get('page', 1, type=int)
    page_size = params.get('page_size', 12, type=int)
    type = params.get('type', 0, type=int)  # 0: all, 1: user, 2: admin
    keyword = params.get('keyword', "", type=str)
    keyword = f"%{keyword}%"

    all_items = User.query

    if keyword:
        all_items = all_items.filter((User.username.like(keyword)))

    if type > 0:
        all_items = all_items.filter((User.is_admin == type - 1))

    total = all_items.count()
    items = all_items.order_by(User.created_date.desc()).paginate(
        page=page, per_page=page_size, error_out=False).items

    results = {
        "items": UserSchema(many=True).dump(items),
        "total": total,
    }

    return send_result(data=results)


@api.route('/<username>', methods=['GET'])
@authorization_require()
def get_user_by_id(username):
    user = User.get_by_id(username)

    return send_result(data=UserSchema().dump(user))


@api.route('/<username>/add-card', methods=['POST'])
@authorization_require()
def create_user(username):
    ret, output = get_json_body(request, AddUserCardValidation)
    if not ret:
        return output

    json_body = output

    card_id = json_body.get("card_id")
    rank = json_body.get("rank")
    if rank > 4:
        rank = 4
    elif rank < 0:
        rank = 0

    card = Card.get_by_id(card_id)
    if not card:
        return send_error()

    attack, defend, army = card.get_attributes_at_rank(rank)
    user_card_id = uuid.uuid1()
    new_user_card = UserCard(id=user_card_id, username=username, card_id=card_id,
                             rank=rank, attack=attack, defend=defend, army=army)
    db.session.add(new_user_card)
    db.session.commit()

    return send_result()

# @api.route('/<user_id>', methods=['PUT'])
# @authorization_require()
# def update_user_admin(user_id):
#     """ This is api for the user management edit the user admin.

#         Request Body:

#         Returns:

#         Examples::

#     """

#     user = User.query.filter_by(id=user_id, type=2).first()
#     if user is None:
#         return send_error(message="Ko ton tai")

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
#     validator_input = CreateUserValidation()
#     is_not_validate = validator_input.validate(json_body)
#     if is_not_validate:
#         return send_error(data=is_not_validate, message_id='11')

#     full_name = json_body.get("full_name")
#     permission_group_id = json_body.get("permission_group_id")
#     is_active: bool = json_body.get("is_active", False)

#     is_clear = False
#     #  change permission group
#     user.full_name = full_name
#     if user.group_id != permission_group_id:
#         is_clear = True
#         user.group_id = permission_group_id

#     user.modified_date = get_timestamp_now()
#     db.session.commit()

#     return send_result(data=UserSchema().dump(user))


# @api.route('/<user_id>', methods=['DELETE'])
# @authorization_require()
# def delete_user_admin(user_id):
#     """ This api for the user management deletes the users.

#         Returns:

#         Examples::

#     """
#     user = User.get_by_id(user_id)
#     if not user:
#         return send_error(message_id="USER_NOT_EXISTED")

#     db.session.delete(user)
#     db.session.commit()

#     return send_result(message_id="DELETED_SUCCESS")


# @api.route('/<user_id>', methods=['GET'])
# @authorization_require()
# def get_user_by_id(user_id):
#     """ This api get information of a user.

#         Returns:

#         Examples::

#     """

#     user = User.get_by_id(user_id)
#     if user:
#         user = UserSchema().dump(user)
#     return send_result(data=user)
