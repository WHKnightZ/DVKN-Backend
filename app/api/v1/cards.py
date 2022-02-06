from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity
from app.api.functions import get_deck
from app.api.helper import get_card_link, send_error, send_result
from app.enums import MSG_OUT_OF_BARREL
from app.gateway import authorization_require
from app.models import Card, User, UserCard
from app.extensions import db

api = Blueprint('cards', __name__)


@api.route('', methods=['GET'])
@authorization_require()
def get_all_cards():
    username = get_jwt_identity()

    user = User.get_by_id(username)

    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 12, type=int)

    total = UserCard.query.count()

    deck = user.deck.split(",")
    items = UserCard.query.filter(UserCard.username == username)\
        .paginate(page=page, per_page=page_size, error_out=False).items

    converted_items = [{"id": item.id,
                        "thumbnail": get_card_link(item.card_id, item.rank),
                        "level": item.level,
                        "attack": item.attack,
                        "defend": item.defend,
                        "army": item.army,
                        "is_in_deck": item.id in deck} for item in items]

    results = {
        "items": converted_items,
        "total": total,
    }

    return send_result(data=results)


@api.route('/deck', methods=['GET'])
@authorization_require()
def get_deck_cards():
    username = get_jwt_identity()

    deck = get_deck(username)

    converted_items = [{"id": item.id,
                        "thumbnail": get_card_link(item.card_id, item.rank),
                        "level": item.level,
                        "attack": item.attack,
                        "defend": item.defend,
                        "army": item.army} for item in deck]

    return send_result(data=converted_items)


@api.route('/<user_card_id>', methods=['GET'])
@authorization_require()
def get_user_card(user_card_id):
    username = get_jwt_identity()
    card = UserCard.query.filter(UserCard.username == username, UserCard.id == user_card_id).first()

    if not card:
        return send_error(message="Thẻ bài không tồn tại")

    card = {"id": card.id,
            "thumbnail": get_card_link(card.card_id, card.rank),
            "level": card.level,
            "attack": card.attack,
            "defend": card.defend,
            "army": card.army}

    return send_result(data=card)


@api.route('/<user_card_id>/upgrage', methods=['PUT'])
@authorization_require()
def upgrage_user_card(user_card_id):
    username = get_jwt_identity()
    user_card = UserCard.query.filter(UserCard.username == username, UserCard.id == user_card_id).first()

    if not user_card:
        return send_error(message="Thẻ bài không tồn tại")

    card = Card.get_by_id(user_card.card_id)

    user = User.get_by_id(username)
    if user.barrel > 0:
        if user_card.level < 15:
            user.barrel -= 1
            # tăng level đồng thời tăng công thủ lính tương ứng
            user_card.level += 1
            user_card.attack += card.attack
            user_card.defend += card.defend
            user_card.army += card.army

            if (user_card.level - 1) % 3 == 0:
                user_card.rank += 1
                # Nếu đây là card trưởng trong deck thì phải update avatar
                if user.deck.split(",")[0] == user_card_id:
                    user.avatar = get_card_link(user_card.card_id, user_card.rank)
            db.session.commit()
            return send_result()
        return send_error()

    return send_error(message_id=MSG_OUT_OF_BARREL, message="Không đủ vò rượu")
