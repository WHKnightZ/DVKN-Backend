from app.models import User, UserCard
from app.extensions import db


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
