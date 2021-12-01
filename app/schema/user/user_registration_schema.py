import re

from marshmallow import Schema, fields, validate, validates, ValidationError


class UserRegistrationSchema(Schema):
    email = fields.String(validate=validate.Email())
    password = fields.String()
    name = fields.String()
    nickname = fields.String()
    mobile_num = fields.String()
    request_id = fields.String(validate=validate.Length(40))

    @validates('mobile_num')
    def validate_mobile_num(self, mobile_num):
        # Mobile number 확인용 정규표현식
        mobile_reg = re.compile(r'^01([0])-?([0-9]{3,4})-?([0-9]{4})$')
        if mobile_reg.match(mobile_num) is None:
            raise ValidationError('Mobile number is invalid')


class UserInfoSchema(Schema):
    email = fields.String()
    name = fields.String()
    nickname = fields.String()
    mobile_num = fields.String()


class UserLoginInfoSchema(Schema):
    email = fields.String()
    name = fields.String()
    nickname = fields.String()
    mobile_num = fields.String()
    access_token = fields.String()
