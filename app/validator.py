from marshmallow import Schema, fields, validate


class UploadValidation(Schema):
    file_name = fields.String(required=True, validate=validate.Length(min=1, max=50))
    prefix = fields.String(required=True)


class MultiUploadValidation(Schema):
    file_names = fields.List(fields.String(required=True))
    prefix = fields.String(required=True)


class AuthValidation(Schema):
    """
    Validator auth
    :param
        username: string
        password: string
    """
    username = fields.String(required=True, validate=[validate.Length(min=1, max=20)])
    password = fields.String(required=True, validate=[validate.Length(min=1, max=16)])


class CreateUserValidation(Schema):
    """
    Validator
    :param
        username: string, required
        password: string, required
    """
    username = fields.String(required=True, validate=validate.Length(min=1, max=36))
    password = fields.String(required=True, validate=validate.Length(min=1, max=16))


class CreateCardValidation(Schema):
    id = fields.String(required=True, validate=validate.Length(min=1, max=50))
    name = fields.String(required=True, validate=validate.Length(min=1, max=50))
    type = fields.Integer(required=True)
    element = fields.Integer(required=True)
    description = fields.String(required=True, validate=validate.Length(min=0, max=500))
    attack = fields.Integer(required=True)
    defend = fields.Integer(required=True)
    army = fields.Integer(required=True)
    probability_register = fields.Integer(required=True)


class UpdateCardValidation(Schema):
    name = fields.String(required=True, validate=validate.Length(min=1, max=50))
    type = fields.Integer(required=True)
    element = fields.Integer(required=True)
    description = fields.String(required=True, validate=validate.Length(min=0, max=500))
    attack = fields.Integer(required=True)
    defend = fields.Integer(required=True)
    army = fields.Integer(required=True)
    probability_register = fields.Integer(required=True)


class ChangePasswordValidation(Schema):
    new_password = fields.String(required=True, validate=validate.Length(min=1, max=16))


class UserSchema(Schema):
    username = fields.String()
    is_admin = fields.Boolean()


class BattleSchema(Schema):
    username = fields.String(required=True, validate=validate.Length(min=1, max=36))
