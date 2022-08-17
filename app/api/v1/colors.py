from uuid import uuid1

from flask import Blueprint, request

from app.api.helper import send_result, get_json_body, send_error
from app.extensions import db
from app.models import Color
from app.utils import get_timestamp_now
from app.validator import ColorSchema

api = Blueprint('colors', __name__)


@api.route('', methods=['POST'])
def create_color():
    ret, output = get_json_body(request, None)
    if not ret:
        return output

    json_body = output

    _id = uuid1()
    _min = json_body.get("min")
    _max = json_body.get("max")
    _color = json_body.get("color")

    created_date = get_timestamp_now()

    new_color = Color(id=_id, min=_min, max=_max, color=_color, created_date=created_date)
    db.session.add(new_color)
    db.session.commit()

    return send_result()


@api.route('', methods=['GET'])
def get_all_colors():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)
    keyword = request.args.get('keyword', "", type=str)
    keyword = f"%{keyword}%"

    all_items = Color.query.filter(Color.color.like(keyword))

    total = all_items.count()

    items = all_items.order_by(Color.min.asc()) \
        .paginate(page=page, per_page=page_size, error_out=False).items

    results = {
        "items": ColorSchema(many=True).dump(items),
        "total": total,
    }

    return send_result(data=results)


@api.route('/<color_id>', methods=['GET'])
def get_color_by_id(color_id):
    item = Color.get_by_id(color_id)
    if not item:
        return send_error()

    return send_result(data=ColorSchema().dump(item))


@api.route('/<color_id>', methods=['PUT'])
def update_color(color_id):
    ret, output = get_json_body(request, None)
    if not ret:
        return output

    json_body = output

    _min = json_body.get("min")
    _max = json_body.get("max")
    _color = json_body.get("color")

    color: Color = Color.get_by_id(color_id)
    if color is None:
        return send_error()

    color.min = _min
    color.max = _max
    color.color = _color

    db.session.commit()

    return send_result()


@api.route('/<color_id>', methods=['DELETE'])
def delete_color(color_id):
    color = Color.query.filter(Color.id == color_id).first()
    if not color:
        return send_error()
    try:
        Color.query.filter(Color.id == color_id).delete()
        db.session.commit()
    except Exception as ex:
        return send_error(message=str(ex))


@api.route('/delete', methods=['POST'])
def delete_colors():
    json_req = request.get_json()

    try:
        Color.query.filter(Color.id.in_(json_req)).delete()
        db.session.commit()
    except Exception as ex:
        return send_error(message=str(ex))

    return send_result()
