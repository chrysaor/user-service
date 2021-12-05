import pytest

from marshmallow.exceptions import MarshmallowError

from app.schema.sms.sms_validation_schema import SmsValidationSchema


def test_sms_validation_schema():
    # Success test
    sms_validation = {
        'sms_type': 'REGISTER',
        'request_id': '0' * 40,
        'mobile_num': '01021290054',
        'auth_code': '013492',
    }

    try:
        schema_obj = SmsValidationSchema().load(sms_validation)
        assert schema_obj.get('sms_type', '') == sms_validation.get('sms_type')
        assert schema_obj.get('request_id', '') == sms_validation.get('request_id')
        assert schema_obj.get('mobile_num', '') == sms_validation.get('mobile_num')
        assert schema_obj.get('auth_code', '') == sms_validation.get('auth_code')
    except MarshmallowError:
        pytest.fail('Schema load error')
    except KeyError:
        pytest.fail('Schema load error')

    # Failure test - sms_type
    sms_validation['sms_type'] = 'RRRRR'

    with pytest.raises(MarshmallowError):
        SmsValidationSchema().load(sms_validation)

    # Failure test - request_id
    sms_validation['sms_type'] = 'LOGIN'
    sms_validation['request_id'] = '0' * 10

    with pytest.raises(MarshmallowError):
        SmsValidationSchema().load(sms_validation)

    # Failure test - mobile_num
    sms_validation['request_id'] = '0' * 40
    sms_validation['mobile_num'] = '0101234'

    with pytest.raises(MarshmallowError):
        SmsValidationSchema().load(sms_validation)

    # Failure test - auth_code
    sms_validation['mobile_num'] = '01012345678'
    sms_validation['auth_code'] = '111'

    with pytest.raises(MarshmallowError):
        SmsValidationSchema().load(sms_validation)

    sms_validation['auth_code'] = '123456779'

    with pytest.raises(MarshmallowError):
        SmsValidationSchema().load(sms_validation)

    sms_validation['auth_code'] = ''

    with pytest.raises(MarshmallowError):
        SmsValidationSchema().load(sms_validation)
