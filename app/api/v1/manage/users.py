import uuid

from flask import Blueprint, request

from app.api.helper import get_json_body, send_error, send_result
from app.enums import MSG_DELETE_SUCCESS, MSG_USER_NOT_EXISTED
from app.extensions import db
from app.models import Card, User, UserCard
from app.validator import AddUserCardValidation, UserSchema
from app.gateway import authorization_require

api = Blueprint('manage/users', __name__)


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
def add_card_to_user(username):
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


@api.route('/<username>', methods=['DELETE'])
@authorization_require()
def delete_user(username):
    user = User.get_by_id(username)
    if not user:
        return send_error(message_id=MSG_USER_NOT_EXISTED)

    db.session.delete(user)
    db.session.commit()

    return send_result(message_id=MSG_DELETE_SUCCESS)
