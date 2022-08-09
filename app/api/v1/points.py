from uuid import uuid1

from flask import Blueprint, request

from app.api.helper import send_result, get_json_body, send_error
from app.extensions import db
from app.models import Point
from app.utils import get_timestamp_now
from app.validator import PointSchema

api = Blueprint('points', __name__)


@api.route('', methods=['POST'])
def create_point():
    ret, output = get_json_body(request, None)
    if not ret:
        return output

    json_body = output

    _id = uuid1()
    name = json_body.get("name")
    layer_id = json_body.get("layer_id")
    long = json_body.get("long")
    lat = json_body.get("lat")
    content = json_body.get("content")
    data = json_body.get("data")

    created_date = get_timestamp_now()

    new_point = Point(id=_id, name=name, layer_id=layer_id, long=long, lat=lat, content=content, data=data,
                      created_date=created_date)
    db.session.add(new_point)
    db.session.commit()

    return send_result()


@api.route('', methods=['GET'])
def get_all_points():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)
    keyword = request.args.get('keyword', "", type=str)
    keyword = f"%{keyword}%"

    all_items = Point.query.filter(Point.name.like(keyword))
    total = all_items.count()

    items = Point.query.filter(Point.name.like(keyword)).order_by(Point.created_date.desc()) \
        .paginate(page=page, per_page=page_size, error_out=False).items

    results = {
        "items": PointSchema(many=True).dump(items),
        "total": total,
    }

    return send_result(data=results)


@api.route('/<point_id>', methods=['GET'])
def get_point_by_id(point_id):
    item = Point.get_by_id(point_id)
    if not item:
        return send_error()

    return send_result(data=PointSchema().dump(item))


@api.route('/<point_id>', methods=['PUT'])
def update_point(point_id):
    ret, output = get_json_body(request, None)
    if not ret:
        return output

    json_body = output

    name = json_body.get("name")
    layer_id = json_body.get("layer_id")
    long = json_body.get("long")
    lat = json_body.get("lat")
    content = json_body.get("content")
    data = json_body.get("data")

    point: Point = Point.get_by_id(point_id)
    if point is None:
        return send_error()

    point.name = name
    point.layer_id = layer_id
    point.long = long
    point.lat = lat
    point.content = content
    point.data = data

    db.session.commit()

    return send_result()


@api.route('/<point_id>', methods=['DELETE'])
def delete_point(point_id):
    point = Point.query.filter(Point.id == point_id).first()
    if not point:
        return send_error()
    try:
        Point.query.filter(Point.id == point_id).delete()
        db.session.commit()
    except Exception as ex:
        return send_error(message=str(ex))


@api.route('/delete', methods=['POST'])
def delete_points():
    json_req = request.get_json()

    try:
        Point.query.filter(Point.id.in_(json_req)).delete()
        db.session.commit()
    except Exception as ex:
        return send_error(message=str(ex))

    return send_result()
