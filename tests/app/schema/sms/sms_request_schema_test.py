import pytest

from marshmallow.exceptions import MarshmallowError

from app.schema.sms.sms_request_schema import SmsRequestSchema


def test_sms_request_schema():
    # Success test
    sms_request = {
        'sms_type': 'REGISTER',
        'email': 'chrysaor@naver.com',
        'name': 'jwkim',
        'nickname': 'jjwwwkim',
        'mobile_num': '01021290054',
    }

    try:
        schema_obj = SmsRequestSchema().load(sms_request)
        assert schema_obj.get('sms_type', '') == sms_request.get('sms_type')
        assert schema_obj.get('email', '') == sms_request.get('email')
        assert schema_obj.get('name', '') == sms_request.get('name')
        assert schema_obj.get('nickname', '') == sms_request.get('nickname')
        assert schema_obj.get('mobile_num', '') == sms_request.get('mobile_num')
    except MarshmallowError:
        pytest.fail('Schema load error')
    except KeyError:
        pytest.fail('Schema load error')

    # Failure test - sms_type
    sms_request['sms_type'] = 'RRRRR'

    with pytest.raises(MarshmallowError):
        SmsRequestSchema().load(sms_request)

    # Failure test - sms_type
    sms_request['sms_type'] = 'LOGIN'
    sms_request['email'] = 'chrysaor@@naver.com'

    with pytest.raises(MarshmallowError):
        SmsRequestSchema().load(sms_request)

    # Failure test - mobile_num
    sms_request['email'] = 'c@d.com'
    sms_request['mobile_num'] = '0101234'

    with pytest.raises(MarshmallowError):
        SmsRequestSchema().load(sms_request)
