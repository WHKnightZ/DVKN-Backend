from flask import Blueprint, request
from app.api.helper import get_card_link, send_error, send_result, get_json_body
from app.enums import MSG_CARD_EXISTED, MSG_CARD_NOT_EXISTED, MSG_DELETE_SUCCESS, MSG_UPDATE_SUCCESS
from app.extensions import db
from app.models import Card
from app.utils import get_timestamp_now
from app.validator import CreateCardValidation, UpdateCardValidation
from app.gateway import authorization_require

api = Blueprint('manage/cards', __name__)


@api.route('', methods=['POST'])
@authorization_require()
def create_card():
    ret, output = get_json_body(request, CreateCardValidation)
    if not ret:
        return output

    json_body = output

    _id = json_body.get("id")
    name = json_body.get("name")
    _type = json_body.get("type")
    element = json_body.get("element")
    description = json_body.get("description")
    attack = json_body.get("attack")
    defend = json_body.get("defend")
    army = json_body.get("army")
    probability_register = json_body.get("probability_register")
    captain_skill = json_body.get("captain_skill")
    specific_skill = json_body.get("specific_skill")

    if probability_register < 0:
        probability_register = 0
    elif probability_register > 100:
        probability_register = 100

    duplicated = Card.get_by_id(_id)
    if duplicated:
        return send_error(message_id=MSG_CARD_EXISTED, message="Thẻ bài đã tồn tại")

    created_date = get_timestamp_now()

    new_card = Card(id=_id, name=name, created_date=created_date, type=_type, element=element, description=description, attack=attack,
                    defend=defend, army=army, probability_register=probability_register, captain_skill=captain_skill, specific_skill=specific_skill)
    db.session.add(new_card)
    db.session.commit()

    return send_result()


@api.route('', methods=['GET'])
@authorization_require()
def get_all_cards():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)
    keyword = request.args.get('keyword', "", type=str)
    keyword = f"%{keyword}%"

    all_items = Card.query.filter(Card.name.like(keyword))
    total = all_items.count()

    items = Card.query.filter(Card.name.like(keyword)).order_by(Card.created_date.desc())\
        .paginate(page=page, per_page=page_size, error_out=False).items

    results = {
        "items": [{"id": item.id, "name": item.name, "type": item.type,
                   "element": item.element, "thumbnail": get_card_link(item.id, 4)} for item in items],
        "total": total,
    }

    return send_result(data=results)


@api.route('/<card_id>', methods=['GET'])
@authorization_require()
def get_card_by_id(card_id):
    item = Card.get_by_id(card_id)
    if not item:
        return send_error(message_id=MSG_CARD_NOT_EXISTED, message="Thẻ bài không tồn tại")

    return send_result(data={"id": item.id, "name": item.name, "type": item.type,
                             "element": item.element, "thumbnail": get_card_link(item.id, "thumbnail"),
                             "description": item.description, "attack": item.attack, "defend": item.defend,
                             "army": item.army, "probability_register": item.probability_register})


@api.route('/<card_id>', methods=['PUT'])
@authorization_require()
def update_card(card_id):
    ret, output = get_json_body(request, UpdateCardValidation)
    if not ret:
        return output

    json_body = output

    name = json_body.get("name")
    _type = json_body.get("type")
    element = json_body.get("element")
    description = json_body.get("description")
    attack = json_body.get("attack")
    defend = json_body.get("defend")
    army = json_body.get("army")
    probability_register = json_body.get("probability_register")
    if probability_register < 0:
        probability_register = 0
    elif probability_register > 100:
        probability_register = 100

    card: Card = Card.get_by_id(card_id)
    if card is None:
        return send_error(message_id=MSG_CARD_NOT_EXISTED, message="Thẻ bài không tồn tại")

    card.name = name
    card.type = _type
    card.element = element
    card.description = description
    card.attack = attack
    card.defend = defend
    card.army = army
    card.probability_register = probability_register

    db.session.commit()

    return send_result(message_id=MSG_UPDATE_SUCCESS)


@api.route('/<card_id>', methods=['DELETE'])
@authorization_require()
def delete_card(card_id):
    card = Card.query.filter(Card.id == card_id).first()
    if not card:
        return send_error(message_id=MSG_CARD_NOT_EXISTED, message="Thẻ bài không tồn tại")
    try:
        Card.query.filter(Card.id == card_id).delete()
        db.session.commit()
    except Exception as ex:
        return send_error(message=str(ex))

    return send_result(message_id=MSG_DELETE_SUCCESS)
