import hashlib
import re

from flask import jsonify

from app.util.error_code import ApiError
from app.util.exception import ApiException


def check_sms_type(sms_type: str):
    """SMS 요청 타입 체크

    Args:
        sms_type(str): SMS 인증 요청 발송 유형

    Raise:
        BadRequestException: SMS 발송 타입이 아닌 경우 발생

    """
    if sms_type not in ['REGISTER', 'LOGIN', 'FIND_PASSWORD']:
        raise ApiException(ApiError.BadRequest)


def check_email(email: str):
    """이메일 규격 체크 함수

    정규식을 통해 이메일을 체크한다.

    Args:
        email(str): 회원 이메일

    Raise:
        BadRequestException: email 길이 혹은 정규식 체크에 실패한 경우 발생

    """
    # Email 확인용 정규표현식
    email_reg = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
    if email_reg.match(email) is None:
        return False

    return True


def check_mobile_num(mobile_num: str):
    """휴대폰 번호 체크 함수

    정규식을 통해 휴대폰 번호를 체크한다.

    Args:
        mobile_num(str): 회원 휴대폰 번호

    Raise:
        BadRequestException: 길이 혹은 정규식 체크에 실패한 경우 발생

    """
    # Mobile number 확인용 정규표현식
    mobile_reg = re.compile(r'^01([0-9])-?([0-9]{3,4})-?([0-9]{4})$')
    if mobile_reg.match(mobile_num) is None:
        raise ApiException(ApiError.BadRequest)


def make_request_id(email: str, name: str, nickname: str, mobile_num: str,
                    timestamp: str):
    """SMS 인증요청 ID 생성 함수

    정규식을 통해 휴대폰 번호를 체크한다.

    Args:
        email(str): 회원 이메일
        name(str): 회원 이름
        nickname(str): 회원 닉네임
        mobile_num(str): 회원 휴대폰 번호
        timestamp(str): Timestamp 문자열 값

    Returns:
        str: Request ID

    """
    # 요청 정보 + 타임스탬프
    source = f'{email}:{name}:{nickname}:{mobile_num}:{timestamp}'

    # Hash 값 계산
    sha1 = hashlib.new('sha1')
    sha1.update(source.encode('utf-8'))

    return sha1.hexdigest()


def init_404_handler(app):
    @app.errorhandler(404)
    def resource_not_found(e):
        message = {
            'message': str(e),
            'error_code': ApiError.ResourceNotFound.get('error_code'),
            'error_message': ApiError.ResourceNotFound.get('error_message')
        }
        return jsonify(message), 404
