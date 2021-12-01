import re

from marshmallow import Schema, fields, validate, validates, ValidationError


class SmsRequestSchema(Schema):
    sms_type = fields.String(
        validate=validate.OneOf(['REGISTER', 'LOGIN', 'FIND_PASSWORD'])
    )
    email = fields.String(
        validate=validate.Email()
    )
    name = fields.String()
    nickname = fields.String()
    mobile_num = fields.String()

    @validates('mobile_num')
    def validate_mobile_num(self, mobile_num):
        # Mobile number 확인용 정규표현식
        mobile_reg = re.compile(r'^01([0])-?([0-9]{3,4})-?([0-9]{4})$')
        if mobile_reg.match(mobile_num) is None:
            raise ValidationError('Mobile number is invalid')
