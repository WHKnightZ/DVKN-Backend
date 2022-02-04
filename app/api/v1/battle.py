import random
from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity
from app.api.helper import get_card_link, get_json_body, send_error, send_result
from app.gateway import authorization_require
from app.models import User, UserCard
from app.validator import BattleSchema
from app.extensions import db

api = Blueprint('battle', __name__)


def random_index(cards):
    indexes = list(filter(lambda x: x != -1, map(lambda card: card[0] if card[1]["hp"] > 0 else -1, enumerate(cards))))
    rd = random.randint(0, len(indexes) - 1)
    return indexes[rd]


def get_deck(username):
    user_cards = db.session.query(User.username, User.deck, UserCard.id, UserCard.card_id, UserCard.rank).join(
        UserCard, User.deck.contains(UserCard.id)).filter(User.username == username).all()

    if (len(user_cards) < 5):
        return

    def find(user_card_id):
        for user_card in user_cards:
            if (user_card.id == user_card_id):
                return user_card

    deck = user_cards[0].deck.split(",")
    new_deck = []
    for user_card_id in deck:
        new_deck.append(find(user_card_id))
    return new_deck


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
