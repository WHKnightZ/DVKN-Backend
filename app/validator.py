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


class UpdateCardValidation(Schema):
    name = fields.String(required=True, validate=validate.Length(min=1, max=50))
    type = fields.Integer(required=True)
    element = fields.Integer(required=True)
    description = fields.String(required=True, validate=validate.Length(min=0, max=500))
    attack = fields.Integer(required=True)
    defend = fields.Integer(required=True)
    army = fields.Integer(required=True)
    probability_register = fields.Integer(required=True)
    captain_skill = fields.String(required=True, validate=validate.Length(min=0, max=500))
    specific_skill = fields.String(required=True, validate=validate.Length(min=0, max=500))


class CreateCardValidation(UpdateCardValidation):
    id = fields.String(required=True, validate=validate.Length(min=1, max=50))


class ChangePasswordValidation(Schema):
    new_password = fields.String(required=True, validate=validate.Length(min=1, max=16))


class UserSchema(Schema):
    username = fields.String()
    is_admin = fields.Boolean()
    avatar = fields.String()
    level = fields.Integer()
    exp = fields.Integer()
    health = fields.Integer()
    gold = fields.Integer()
    diamond = fields.Integer()
    barrel = fields.Integer()
    total_battle = fields.Integer()
    win_battle = fields.Integer()


class BattleSchema(Schema):
    username = fields.String(required=True, validate=validate.Length(min=1, max=36))


class AddUserCardValidation(Schema):
    card_id = fields.String(required=True, validate=validate.Length(min=1, max=50))
    rank = fields.Integer(required=True)


class LayerSchema(Schema):
    id = fields.String()
    name = fields.String()
    icon = fields.String()
    content = fields.String()
    form = fields.String()
    created_date = fields.Integer()


class PointSchema(Schema):
    id = fields.String()
    name = fields.String()
    long = fields.Integer()
    lat = fields.Integer()
    content = fields.String()
    data = fields.String()
    created_date = fields.Integer()
    layer = fields.Nested(LayerSchema(exclude=["created_date", "content"]))


class ColorSchema(Schema):
    id = fields.String()
    min = fields.Integer()
    max = fields.Integer()
    color = fields.String()
    created_date = fields.Integer()
