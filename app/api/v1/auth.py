from datetime import timedelta
import uuid

from flask import Blueprint, request
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_jwt_identity, jwt_refresh_token_required)
from werkzeug.security import check_password_hash, generate_password_hash

from app.api.helper import get_card_link, get_json_body, send_error, send_result
from app.enums import MSG_INCORRECT_AUTH, MSG_USER_EXISTED
from app.extensions import db
from app.models import Card, User, UserCard
from app.utils import get_timestamp_now, random_card_register
from app.validator import AuthValidation, UserSchema

ACCESS_EXPIRES = timedelta(days=1)
REFRESH_EXPIRES = timedelta(days=5)

api = Blueprint('auth', __name__)


@api.route('/sign-up', methods=['POST'])
def sign_up():
    ret, output = get_json_body(request, AuthValidation)
    if not ret:
        return output

    json_body = output

    username = json_body.get("username")
    password = json_body.get("password")
    duplicated_user = User.query.filter(User.username == username).first()
    if duplicated_user:
        return send_error(message_id=MSG_USER_EXISTED, message="Tài khoản đã tồn tại")

    created_date = get_timestamp_now()
    deck = []
    cards = Card.query.all()
    user_cards = random_card_register(cards)

    for user_card in user_cards:
        card = user_card["card"]
        rank = user_card["rank"]
        user_card_id = uuid.uuid1()
        user_card["id"] = user_card_id
        new_user_card = UserCard(id=user_card_id, username=username, card_id=card.id,
                                 rank=rank, attack=0, defend=0, army=0)
        db.session.add(new_user_card)
        deck.append(str(user_card_id))

    deck = ",".join(deck)
    new_user = User(username=username, password_hash=generate_password_hash(
        password), deck=deck, created_date=created_date)
    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(identity=username, expires_delta=ACCESS_EXPIRES)
    refresh_token = create_refresh_token(identity=username, expires_delta=REFRESH_EXPIRES)

    data = {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "username": username,
        "card_images": [{"id": item["id"], "image": get_card_link(item["card"].id, item["rank"])} for item in user_cards]
    }

    return send_result(data=data)


@api.route('/sign-in', methods=['POST'])
def sign_in():
    ret, output = get_json_body(request, AuthValidation)
    if not ret:
        return output

    json_body = output

    # Check username and password
    username = json_body.get("username")
    password = json_body.get("password")

    user = User.query.filter(User.username == username).first()
    if user is None or (password and not check_password_hash(user.password_hash, password)):
        return send_error(message_id=MSG_INCORRECT_AUTH, message="Sai tài khoản hoặc mật khẩu")

    access_token = create_access_token(identity=user.username, expires_delta=ACCESS_EXPIRES,
                                       user_claims={"is_admin": user.is_admin})
    refresh_token = create_refresh_token(identity=user.username, expires_delta=REFRESH_EXPIRES,
                                         user_claims={"is_admin": user.is_admin})

    data: dict = UserSchema().dump(user)
    data.setdefault('access_token', access_token)
    data.setdefault('refresh_token', refresh_token)

    return send_result(data=data, message="Ok")


@api.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    user_identity = get_jwt_identity()
    user = User.get_by_id(user_identity)

    access_token = create_access_token(identity=user.username, expires_delta=ACCESS_EXPIRES,
                                       user_claims={"is_admin": user.is_admin})

    data = {
        'access_token': access_token
    }

    return send_result(data=data)
