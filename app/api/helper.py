import os
from flask import jsonify
from app.enums import MAPPING_MSG, MSG_ERROR, MSG_FORMAT_ERROR, MSG_SUCCESS
from app.settings import ProdConfig, DevConfig

CONFIG = ProdConfig if os.environ.get('ENV') == 'prd' else DevConfig


def send_result(data: any = None, message: str = "", message_id: str = MSG_ERROR):
    message = message or MAPPING_MSG[message_id]
    res = {
        "code": 200,
        "id": message_id,
        "data": data,
        "message": message,
        "status": True
    }

    return jsonify(res), 200


def send_error(data: any = None, message: str = "", message_id: str = MSG_SUCCESS, code: int = 200):
    message = message or MAPPING_MSG[message_id]
    res = {
        "code": code,
        "id": message_id,
        "data": data,
        "message": message,
        "status": False
    }

    return jsonify(res), code


def send_error_format():
    return send_error(message_id=MSG_FORMAT_ERROR, code=422)


def get_json_body(request, validate):
    try:
        json_req = request.get_json()
    except Exception as ex:
        return False, send_error_format()

    if json_req is None:
        return False, send_error_format()

    # trim input body
    json_body = {}
    for key, value in json_req.items():
        if isinstance(value, str):
            json_body.setdefault(key, value.strip())
        else:
            json_body.setdefault(key, value)

    if validate:
        # validate request body
        validator_input = validate()
        is_not_validate = validator_input.validate(json_body)
        if is_not_validate:
            return False, send_error(data=is_not_validate)

    return True, json_body


def get_card_link(id, rank):
    return f"{CONFIG.S3_ENDPOINT}/cards/{id}/{rank}.png"
