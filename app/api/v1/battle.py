import random
from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity
from app.api.functions import get_deck
from app.api.helper import get_card_link, get_json_body, send_error, send_result
from app.gateway import authorization_require
from app.models import User
from app.validator import BattleSchema
from app.extensions import db

api = Blueprint('battle', __name__)


def random_index(cards):
    indexes = list(filter(lambda x: x != -1, map(lambda card: card[0] if card[1]["hp"] > 0 else -1, enumerate(cards))))
    rd = random.randint(0, len(indexes) - 1)
    return indexes[rd]


@api.route('/users', methods=['GET'])
@authorization_require()
def get_all_battle_users():
    username = get_jwt_identity()

    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 12, type=int)
    keyword = request.args.get('keyword', "", type=str)
    keyword = f"%{keyword}%"

    all_items = User.query.filter((User.username.like(keyword)), User.is_admin == 0)
    total = all_items.count()

    # items = db.session.query(User.username, UserCard.card_id, UserCard.rank).join(UserCard, func.substring(
    #     User.deck, 1, 36) == UserCard.id).filter((User.username.like(keyword)), User.is_admin == 0, User.username != username)\
    #     .order_by(User.created_date.desc()).paginate(page=page, per_page=page_size,
    #                                                  error_out=False).items
    items = db.session.query(User.username).filter((User.username.like(keyword)), User.is_admin == 0, User.username != username)\
        .order_by(User.created_date.desc()).paginate(page=page, per_page=page_size, error_out=False).items

    results = {
        "items": [{"username": item.username,
                   "avatar": item.avatar,
                   "level": item.level,
                   "win_battle": item.win_battle,
                   "total_battle": item.total_battle} for item in items],
        "total": total,
    }

    return send_result(data=results)


@api.route('', methods=['POST'])
@authorization_require()
def battle():
    ret, output = get_json_body(request, BattleSchema)
    if not ret:
        return output

    json_body = output

    attacker = get_jwt_identity()
    defender = json_body.get("username")

    attacker_cards = get_deck(attacker)
    defender_cards = get_deck(defender)

    if not attacker_cards or not defender_cards:
        return send_error(message="Thông tin không hợp lệ")

    players = [attacker_cards, defender_cards]

    players = [
        {
            "cards": [{
                "image": get_card_link(card.card_id, card.rank),
                "atk": random.randint(200, 400),
                "hp": random.randint(600, 1000)
            } for card in player],
            "death": 0
        } for player in players]

    players_info = list(map(lambda x: {"cards": list(map(lambda y: {**y, "max_hp": y["hp"]}, x["cards"]))}, players))

    battle_result = []
    attacking_player = 0
    while players[0]["death"] < 5 and players[1]["death"] < 5:
        defending_player = 1 - attacking_player
        attacking_index = random_index(players[attacking_player]["cards"])
        defending_index = random_index(players[defending_player]["cards"])

        players[defending_player]["cards"][defending_index]["hp"] -= \
            players[attacking_player]["cards"][attacking_index][
                "atk"]
        if players[defending_player]["cards"][defending_index]["hp"] <= 0:
            players[defending_player]["death"] += 1

        battle_result.append({
            "atk_card": attacking_index,
            "def_card": defending_index,
        })

        attacking_player = 1 - attacking_player

    return send_result(data={
        "players": players_info,
        "battle_result": battle_result,
        "winner": 1 - attacking_player,
        "turns": len(battle_result)
    })
