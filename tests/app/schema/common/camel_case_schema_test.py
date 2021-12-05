import pytest
from marshmallow import fields

from marshmallow.exceptions import MarshmallowError

from app.schema.common.CamelCaseSchema import CamelCaseSchema


def test_camel_case_schema():
    # Success test
    class TestSchema(CamelCaseSchema):
        snake_case = fields.Str()
        is_it_snake_case = fields.Str()

    snake_case = {
        'snake_case': 'yes',
        'is_it_snake_case': 'yes',
    }

    try:
        schema_obj = TestSchema().dump(snake_case)
        assert schema_obj.get('snakeCase', '') == snake_case.get('snake_case')
        assert schema_obj.get('isItSnakeCase', '') == snake_case.get('is_it_snake_case')
    except MarshmallowError:
        pytest.fail('Schema load error')
