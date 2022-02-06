import boto3
from botocore.config import Config
from flask import Blueprint, request

from app.api.helper import get_json_body, send_result, send_error, CONFIG
from app.validator import MultiUploadValidation, UploadValidation

api = Blueprint('upload', __name__)

s3 = boto3.client('s3', region_name=CONFIG.AWS_REGION_NAME, endpoint_url=CONFIG.S3_ENDPOINT,
                  config=Config(signature_version='s3v4'))


def generate_link(prefix, file_name):
    url = s3.generate_presigned_url(
        ClientMethod='put_object',
        Params={
            'Bucket': prefix,
            'Key': file_name,
            'ACL': 'public-read'
        },
        ExpiresIn=3600,
    )

    return url, '{}/{}/{}'.format(CONFIG.S3_ENDPOINT, prefix, file_name)


@api.route('', methods=['GET'])
def generate_pre_signed_url():
    prefix = request.args.get('prefix', "", type=str).strip()
    file_name = request.args.get('file_name', "", type=str).strip()

    # validate request params
    validator_upload = UploadValidation()
    is_invalid = validator_upload.validate({"file_name": file_name, "prefix": prefix})
    if is_invalid:
        return send_error(data=is_invalid, message='Please check your request params')

    upload_link, file_link = generate_link(prefix, file_name)
    data = dict(upload_link=upload_link, file_link=file_link)

    return send_result(data=data, message="Generate pre signed url successfully")


@api.route('', methods=['POST'])
def generate_multi_pre_signed_urls():
    ret, output = get_json_body(request, MultiUploadValidation)
    if not ret:
        return output

    json_body = output

    file_names = json_body.get("file_names")
    prefix = json_body.get("prefix")

    arr = [""] * len(file_names)

    for index, file_name in enumerate(file_names):
        upload_link, file_link = generate_link(prefix, file_name)
        data = dict(upload_link=upload_link, file_link=file_link)
        arr[index] = data

    return send_result(data=arr, message="Generate multi pre signed urls successfully")
