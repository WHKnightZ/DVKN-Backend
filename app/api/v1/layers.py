from uuid import uuid1

from flask import Blueprint, request

from app.api.helper import send_result, get_json_body, send_error
from app.extensions import db
from app.models import Layer
from app.utils import get_timestamp_now

api = Blueprint('layers', __name__)


@api.route('', methods=['POST'])
def create_layer():
    ret, output = get_json_body(request, None)
    if not ret:
        return output

    json_body = output

    _id = uuid1()
    name = json_body.get("name")
    icon = json_body.get("icon")
    content = json_body.get("content")
    form = json_body.get("form")

    created_date = get_timestamp_now()

    new_layer = Layer(id=_id, name=name, form=form, icon=icon, content=content,
                      created_date=created_date)
    db.session.add(new_layer)
    db.session.commit()

    return send_result()


@api.route('', methods=['GET'])
def get_all_layers():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)
    keyword = request.args.get('keyword', "", type=str)
    keyword = f"%{keyword}%"

    all_items = Layer.query.filter(Layer.name.like(keyword))
    total = all_items.count()

    items = Layer.query.filter(Layer.name.like(keyword)).order_by(Layer.created_date.desc()) \
        .paginate(page=page, per_page=page_size, error_out=False).items

    results = {
        "items": [{"id": item.id, "name": item.name, "icon": item.icon, "content": item.content, "form": item.form,
                   "created_date": item.created_date} for item in items],
        "total": total,
    }

    return send_result(data=results)


@api.route('/<layer_id>', methods=['GET'])
def get_layer_by_id(layer_id):
    item = Layer.get_by_id(layer_id)
    if not item:
        return send_error()

    return send_result(
        data={"id": item.id, "name": item.name, "icon": item.icon, "content": item.content, "form": item.form,
              "created_date": item.created_date})


@api.route('/<layer_id>', methods=['PUT'])
def update_layer(layer_id):
    ret, output = get_json_body(request, None)
    if not ret:
        return output

    json_body = output

    name = json_body.get("name")
    icon = json_body.get("icon")
    content = json_body.get("content")
    form = json_body.get("form")

    layer: Layer = Layer.get_by_id(layer_id)
    if layer is None:
        return send_error()

    layer.name = name
    layer.icon = icon
    layer.content = content
    layer.form = form

    db.session.commit()

    return send_result()


@api.route('/<layer_id>', methods=['DELETE'])
def delete_layer(layer_id):
    layer = Layer.query.filter(Layer.id == layer_id).first()
    if not layer:
        return send_error()
    try:
        Layer.query.filter(Layer.id == layer_id).delete()
        db.session.commit()
    except Exception as ex:
        return send_error(message=str(ex))


@api.route('/delete', methods=['POST'])
def delete_layers():
    json_req = request.get_json()

    try:
        Layer.query.filter(Layer.id.in_(json_req)).delete()
        db.session.commit()
    except Exception as ex:
        return send_error(message=str(ex))

    return send_result()
