from uuid import uuid1

from flask import Blueprint, request

from app.api.helper import send_result, get_json_body, send_error
from app.extensions import db
from app.models import WM_Layout
from app.utils import get_timestamp_now

api = Blueprint('wm_layouts', __name__)


@api.route('', methods=['POST'])
def create_layout():
    ret, output = get_json_body(request, None)
    if not ret:
        return output

    json_body = output

    _id = uuid1()
    title = json_body.get("title")
    config_data = json_body.get("configData")
    description = json_body.get("description")
    cols = json_body.get("cols")
    rows = json_body.get("rows")

    created_date = get_timestamp_now()

    new_layout = WM_Layout(id=_id, title=title, config_data=config_data, description=description, cols=cols, rows=rows,
                           created_date=created_date)
    db.session.add(new_layout)
    db.session.commit()

    return send_result()


@api.route('/list', methods=['POST'])
def get_all_layouts():
    ret, output = get_json_body(request, None)
    if not ret:
        return output

    json_body = output

    page = json_body.get("pageNumber", 1)
    page_size = json_body.get("pageSize", 10)
    keyword = json_body.get("keyword", "")
    filter_params = json_body.get("filterParam", [])
    sort = json_body.get("sortingParams", [{"sortOrder": 2, "columnName": "created_date"}])

    keyword = f"%{keyword}%"
    sort = sort[0]
    sort_order = sort["sortOrder"]
    sort_column = sort["columnName"]

    all_items = WM_Layout.query.filter(WM_Layout.title.like(keyword))
    for f in filter_params:
        column_name = f["columnName"]
        filter_value = f["filterValue"]
        if column_name == "title":
            all_items = all_items.filter(WM_Layout.title.like(f"%{filter_value}%"))

    total = all_items.count()

    items = all_items

    sort_query = WM_Layout.created_date
    if sort_column == "title":
        sort_query = WM_Layout.title
    if sort_order == 1:
        sort_query = sort_query.asc()
    else:
        sort_query = sort_query.desc()

    items = items.order_by(sort_query).paginate(page=page, per_page=page_size, error_out=False).items

    results = {
        "items": [{"id": item.id, "title": item.title, "configData": item.config_data, "description": item.description,
                   "created_date": item.created_date} for
                  item in items],
        "totalCount": total,
    }

    return send_result(data=results)


@api.route('/<layout_id>', methods=['GET'])
def get_layout_by_id(layout_id):
    item = WM_Layout.get_by_id(layout_id)
    if not item:
        return send_error()

    return send_result(
        data={"id": item.id, "title": item.title, "configData": item.config_data, "description": item.description,
              "cols": item.cols, "rows": item.rows,
              "created_date": item.created_date})


@api.route('/<layout_id>', methods=['PUT'])
def update_layout(layout_id):
    ret, output = get_json_body(request, None)
    if not ret:
        return output

    json_body = output

    title = json_body.get("title")
    config_data = json_body.get("configData")
    description = json_body.get("description")

    layout: WM_Layout = WM_Layout.get_by_id(layout_id)
    if layout is None:
        return send_error()

    layout.title = title
    layout.config_data = config_data
    layout.description = description

    db.session.commit()

    return send_result()


@api.route('', methods=['DELETE'])
def delete_layouts():
    json_req = request.get_json()

    try:
        WM_Layout.query.filter(WM_Layout.id.in_(json_req)).delete()
        db.session.commit()
    except Exception as ex:
        return send_error(message=str(ex))

    return send_result()
