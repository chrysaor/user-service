from datetime import datetime

import pytest

from app.util.common import check_email, check_sms_type, check_mobile_num, make_request_id
from app.util.exception import ApiException


def test_check_email():
    """이메일 체크 테스트"""
    assert(check_email('chrysaor@naver.com') is True)
    assert(check_email('chrysaor@@naver.com') is False)
    assert(check_email('chrysaor@naver') is False)
    assert(check_email('chrysaor') is False)
    assert(check_email('c@') is False)
    assert(check_email('') is False)


def test_check_sms_type():
    """SMS type 체크 테스트"""
    # Success
    try:
        check_sms_type('LOGIN')
        check_sms_type('REGISTER')
        check_sms_type('FIND_PASSWORD')
    except ApiException:
        pytest.fail('ApiException test fail')

    # Failed test
    pytest.raises(ApiException, check_sms_type, 'REGIS')
    pytest.raises(ApiException, check_sms_type, '')
    pytest.raises(ApiException, check_sms_type, 'LOGIN_')


def test_check_mobile_num():
    """휴대폰 번호 체크 테스트

    010XXXXXXXX, 예전 휴대폰 번호도 허용

    """
    # Success test
    try:
        check_mobile_num('01011110054')
        check_mobile_num('01021990054')
        check_mobile_num('01029384921')
        check_mobile_num('0110090054')
    except ApiException:
        pytest.fail('ApiException test fail')

    # Failed test
    pytest.raises(ApiException, check_mobile_num, '0102129')
    pytest.raises(ApiException, check_mobile_num, '010')
    pytest.raises(ApiException, check_mobile_num, '11010239')


def test_make_request_id():
    """요청 ID 생성함수 테스트"""
    today = str(datetime.today().timestamp())
    req_id = make_request_id(
        'chrysaor@naver.com', 'JaewooKim', 'Nickanme', '01021290054', today
    )

    assert len(req_id) == 40
