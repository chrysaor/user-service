import pytest

from marshmallow.exceptions import MarshmallowError

from app.schema.user.user_registration_schema import UserRegistrationSchema


def test_user_registration_schema():
    # Success test
    user_registration = {
        'email': 'chrysaor@naver.com',
        'password': 'test1234',
        'name': 'jwkim',
        'nickname': 'jjwwkim',
        'mobile_num': '01021290054',
        'request_id': '0' * 40,
    }

    try:
        schema_obj = UserRegistrationSchema().load(user_registration)
        assert schema_obj.get('email', '') == user_registration.get('email')
        assert schema_obj.get('password', '') == user_registration.get('password')
        assert schema_obj.get('name', '') == user_registration.get('name')
        assert schema_obj.get('nickname', '') == user_registration.get('nickname')
        assert schema_obj.get('mobile_num', '') == user_registration.get('mobile_num')
        assert schema_obj.get('request_id', '') == user_registration.get('request_id')
    except MarshmallowError:
        pytest.fail('Schema load error')
    except KeyError:
        pytest.fail('Schema load error')

    # Failure test - email
    user_registration['email'] = 'cccc@@d'

    with pytest.raises(MarshmallowError):
        UserRegistrationSchema().load(user_registration)

    # Failure test - request_id
    user_registration['email'] = 'a@a.com'
    user_registration['request_id'] = '0'

    with pytest.raises(MarshmallowError):
        UserRegistrationSchema().load(user_registration)

    # Failure test - mobile_num
    user_registration['request_id'] = '0' * 40
    user_registration['mobile_num'] = '010'

    with pytest.raises(MarshmallowError):
        UserRegistrationSchema().load(user_registration)
