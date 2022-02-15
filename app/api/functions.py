from app.enums import HEALTH_INCREASE, HEALTH_INTERVAL
from app.models import User, UserCard
from app.extensions import db, user_healths
from app.utils import get_timestamp_now
import math


def get_deck(username):
    user_cards = db.session.query(User.username, User.deck, UserCard.id, UserCard.card_id, UserCard.rank,
                                  UserCard.level, UserCard.attack, UserCard.defend, UserCard.army).join(
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


def update_user_health(username):
    health = user_healths.get(username, None)
    now = get_timestamp_now()

    if health is None:
        health = User.get_by_id(username).health
        health = (health, health, now)  # current_health, max_health, last_time

    current_health, max_health, last_time = health

    if current_health < max_health:
        increase = (now - last_time) // HEALTH_INTERVAL
        if increase > 0:
            current_health += increase * HEALTH_INCREASE
            current_health = min(current_health, max_health)
            last_time += increase * HEALTH_INCREASE

    user_healths[username] = (current_health, max_health, last_time)


def get_user_health(username):
    return user_healths.get(username, None)


def get_time_full_health(username):
    # trả lại thời gian đầy máu: số giây cần và timestamp đầy máu
    now = get_timestamp_now()
    current_health, max_health, last_time = get_user_health(username)

    if current_health < max_health:
        interval = math.ceil((max_health - current_health) / HEALTH_INCREASE)
        interval *= HEALTH_INTERVAL
        interval += last_time - now
        return (current_health, max_health, interval)
    else:
        return (current_health, max_health, 0)


def user_lose_health(username, health):
    now = get_timestamp_now()
    current_health, max_health, last_time = get_user_health(username)
    if current_health < health:
        return False, current_health

    if current_health == max_health:
        last_time = now

    current_health -= health
    user_healths[username] = (current_health, max_health, last_time)

    return True, current_health
