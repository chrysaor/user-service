from marshmallow import Schema, fields


class LoginRequestSchema(Schema):
    id = fields.Str()
    password = fields.Str()
