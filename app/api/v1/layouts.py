from uuid import uuid1

from flask import Blueprint, request

from app.api.helper import send_result, get_json_body, send_error
from app.extensions import db
from app.models import Layout
from app.utils import get_timestamp_now

api = Blueprint('layouts', __name__)


@api.route('', methods=['POST'])
def create_layout():
    ret, output = get_json_body(request, None)
    if not ret:
        return output

    json_body = output

    _id = uuid1()
    title = json_body.get("title")
    data = json_body.get("data")
    created_date = get_timestamp_now()

    new_layout = Layout(id=_id, title=title, data=data, created_date=created_date)
    db.session.add(new_layout)
    db.session.commit()

    return send_result()


@api.route('', methods=['GET'])
def get_all_layouts():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)
    keyword = request.args.get('keyword', "", type=str)
    keyword = f"%{keyword}%"

    all_items = Layout.query.filter(Layout.title.like(keyword))
    total = all_items.count()

    items = Layout.query.filter(Layout.title.like(keyword)).order_by(Layout.created_date.desc()) \
        .paginate(page=page, per_page=page_size, error_out=False).items

    results = {
        "items": [{"id": item.id, "title": item.title, "data": item.data} for item in items],
        "total": total,
    }

    return send_result(data=results)


@api.route('/<layout_id>', methods=['GET'])
def get_layout_by_id(layout_id):
    item = Layout.get_by_id(layout_id)
    if not item:
        return send_error()

    return send_result(data={"id": item.id, "title": item.title, "data": item.data})


@api.route('/<layout_id>', methods=['PUT'])
def update_layout(layout_id):
    ret, output = get_json_body(request, None)
    if not ret:
        return output

    json_body = output

    title = json_body.get("title")
    data = json_body.get("data")

    layout: Layout = Layout.get_by_id(layout_id)
    if layout is None:
        return send_error()

    layout.title = title
    layout.data = data

    db.session.commit()

    return send_result()


@api.route('/<layout_id>', methods=['DELETE'])
def delete_layout(layout_id):
    layout = Layout.query.filter(Layout.id == layout_id).first()
    if not layout:
        return send_error()
    try:
        Layout.query.filter(Layout.id == layout_id).delete()
        db.session.commit()
    except Exception as ex:
        return send_error(message=str(ex))

    return send_result()
