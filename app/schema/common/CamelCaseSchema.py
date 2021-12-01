from marshmallow import Schema, fields


def camelcase(s):
    parts = iter(s.split('_'))
    return next(parts) + ''.join(i.title() for i in parts)


class CamelCaseSchema(Schema):
    """카멜 케이스로 변환하는 스키마"""
    def on_bind_field(self, field_name: str, field_obj: fields.Field) -> None:
        field_obj.data_key = camelcase(field_obj.data_key or field_name)
