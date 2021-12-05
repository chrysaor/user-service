import pytest

from marshmallow.exceptions import MarshmallowError

from app.schema.auth.find_password_schema import FindPasswordSchema


def test_find_password_schema():
    # Success test
    find_password = {
        'email': 'chrysaor@naver.com',
        'mobile_num': '01021290054',
        'request_id': '0' * 40
    }

    try:
        schema_obj = FindPasswordSchema().load(find_password)
        assert schema_obj.get('email', '') == find_password.get('email')
        assert schema_obj.get('mobile_num', '') == find_password.get('mobile_num')
        assert schema_obj.get('request_id', '') == find_password.get('request_id')
    except MarshmallowError:
        pytest.fail('Schema load error')

    # Failure test - email
    find_password['email'] = 'chrysaor@@naver.com'

    with pytest.raises(MarshmallowError):
        FindPasswordSchema().load(find_password)

    # Failure test - request_id
    find_password['email'] = 'chrysaor@naver.com'
    find_password['request_id'] = '0' * 10

    with pytest.raises(MarshmallowError):
        FindPasswordSchema().load(find_password)

    # Failure test - mobile_num
    find_password['request_id'] = '0' * 40
    find_password['mobile_num'] = '11112345'

    with pytest.raises(MarshmallowError):
        FindPasswordSchema().load(find_password)
