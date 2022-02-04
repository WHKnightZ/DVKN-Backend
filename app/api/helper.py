import os
from flask import jsonify
from app.settings import ProdConfig, DevConfig

CONFIG = ProdConfig if os.environ.get('ENV') == 'prd' else DevConfig


def send_result(data: any = None, message: str = "Thành công", message_id: str = ''):
    res = {
        "code": 200,
        "id": message_id,
        "data": data,
        "message": message,
        "status": True
    }

    return jsonify(res), 200


def send_error(data: any = None, message: str = "Có lỗi xảy ra", message_id: str = '', code: int = 200):
    res = {
        "code": code,
        "id": message_id,
        "data": data,
        "message": message,
        "status": False
    }

    return jsonify(res), code


def send_error_format():
    return send_error(message='Nội dung gửi đi không hợp lệ', code=422)


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
            return False, send_error(data=is_not_validate, message_id='0')

    return True, json_body


def get_card_link(id, rank):
    return f"{CONFIG.S3_ENDPOINT}/cards/{id}/{rank}.png"
