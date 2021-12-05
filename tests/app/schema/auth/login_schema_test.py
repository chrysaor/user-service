import pytest

from marshmallow.exceptions import MarshmallowError

from app.schema.auth.login_schema import LoginRequestSchema


def test_login_request_schema():
    # Success test
    login_request = {
        'id': 'chrysaor@naver.com',
        'password': 'test1234',
    }

    try:
        schema_obj = LoginRequestSchema().load(login_request)
        assert schema_obj.get('id', '') == login_request.get('id')
        assert schema_obj.get('password', '') == login_request.get('password')
    except MarshmallowError:
        pytest.fail('Schema load error')
