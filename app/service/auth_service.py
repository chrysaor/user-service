import json
import re
import jwt

from datetime import datetime
from typing import Dict

from dateutil.relativedelta import relativedelta
from flask import Request, g
from flask_restx import abort
from marshmallow import ValidationError

from app.database.models import session_scope
from app.model.user.user import User
from app.model.user.user_sms_request import UserSmsRequest
from app.schema.auth.find_password_schema import FindPasswordSchema
from app.schema.user.user_registration_schema import UserLoginInfoSchema, UserInfoSchema
from app.util.constants import Constants, template
from app.util.common import check_email
from app.util.error_code import AuthError, TokenError, ApiError
from app.util.exception import ApiException, v_msg


def user_login(user_id: str, password: str) -> Dict:
    """유저 로그인

    사용자 아이디와 패스워드를 체크하여 통과하면 인증 정보를 전달한다.

    Args:
        user_id(str): 유저 아이디. 이메일과 휴대폰 번호로 로그인 가능.
        password (str): 유저 패스워드.

    Returns:
        response (dict): 로그인 응답 값

    Raises:
        LoginException: 유저가 없거나 비밀번호가 틀린 경우 발생
    """
    try:
        with session_scope() as loc_session:
            user_query = loc_session.query(User).filter()

            if check_email(user_id):
                user_query.filter(User.email == user_id)
            else:
                user_query.filter(User.mobile_num == user_id)

            # User instance
            user_ins = user_query.first()

            # 유저가 없거나 패스워드가 틀린 경우
            if user_ins is None or not user_ins.check_password(password):
                raise ApiException(AuthError.UserNotFound)

            # 토큰 생성 및 업데이트
            access_token = encode_auth_token(user_ins.id)
            user_ins.access_token = access_token

            # Schema dump
            user_data = UserLoginInfoSchema().dumps(user_ins)

        return json.loads(user_data)
    except ApiException as ex:
        return abort(ex.code, ex.message, **ex.to_json())
    except BaseException as ex:
        details = template.format(type(ex).__name__, ex.args)
        return abort(500, '로그인 중 오류가 발생하였습니다.', details=details)


def logout_user() -> Dict:
    """로그아웃 API

    로그인 토큰을 받고, 해당 회원의 아이디를 찾아 토큰을 삭제한다.

    Returns:
        Dict: 응답 dictionary
    """
    try:
        user_id = g.get('user_id')
        token = g.get('user_token')

        with session_scope() as loc_session:
            User.clear_token(loc_session, user_id, token)

        return {'result': 'success'}
    except ApiException as ex:
        return abort(ex.code, ex.message, **ex.to_json())
    except BaseException as ex:
        details = template.format(type(ex).__name__, ex.args)
        return abort(500, '로그아웃 중 오류가 발생하였습니다.', details=details)


def get_logged_in_user():
    """
    토큰 확인하여 로그인한 사용자의 정보를 조회
    """
    try:
        # 인증 토큰 가져오기
        user_id = g.get('user_id')

        with session_scope() as loc_session:
            user = User.get_user_by_id(loc_session, user_id)
            result = UserInfoSchema().dumps(user)

        return json.loads(result)
    except ApiException as ex:
        return abort(ex.code, ex.message, **ex.to_json())
    except Exception as ex:
        details = template.format(type(ex).__name__, ex.args)
        return abort(500, '사용자 정보 조회 중 오류가 발생하였습니다.', details=details)


def encode_auth_token(user_id: str) -> bytes:
    """인증 토큰 생성

    인코딩 과정에서의 payload type:
    --------------------------
        iss: 토큰 발급자(issuer)
        sub: 토큰 제목(subject)
        aud: 토큰 대상자(audience)
        exp: 토큰 만료 시간(expiration),
            NumericDate 형식으로 되어 있어야 함
            ex) 1480849147370
        nbf: 토큰 활성 날짜(not before),
            이 날이 지나기 전의 토큰은 활성화되지 않음
        iat: 토큰 발급 시간(issued at), 토큰 발급 이후의 경과 시간을 알 수 있음
        jti: JWT 토큰 식별자(JWT ID),
            중복 방지를 위해 사용하며, 일회용 토큰(Access Token) 등에 사용
    Returns
        str: 토큰 대상자 (회원 아이디)

    """
    try:
        payload = {
            'exp': datetime.utcnow() + relativedelta(minutes=3000),  # 토큰 유효기간 설정
            'iat': datetime.utcnow(),
            'sub': user_id,
        }
        return jwt.encode(payload, "secret", algorithm="HS256")
    except Exception as ex:
        details = template.format(type(ex).__name__, ex.args)
        return abort(500, '토큰 인코딩 처리 중 오류가 발생하였습니다.', details=details)


def decode_auth_token(request: Request) -> Dict:
    """인증토큰 디코딩

    JWT 토큰 디코딩 후 발급자 반환

    Args:
        request(Request): 요청 객체

    Returns:
        Dict: 유저 아이디 및 토큰
    """
    try:
        auth_token = request.headers.get("Authorization").split(" ")[1]
        payload = jwt.decode(auth_token, 'secret', algorithms="HS256")
        return {'user_id': payload['sub'], "access_token": auth_token}
    except jwt.ExpiredSignatureError:
        raise ApiException(TokenError.TokenExpired)
    except jwt.InvalidTokenError:
        raise ApiException(TokenError.InvalidToken)
    except BaseException:
        raise ApiException(ApiError.BadRequest)


def validate_password(password: str) -> bool:
    """비밀번호 유효성 검사

    Args:
        password(str): 패스워드

    Returns:
        bool: 통과하면 True

    Raises:
        ApiException: 각 예외별 메시지로 구분
    """
    password_length = 8

    if len(password) < password_length:
        raise ApiException({'error_message': '비밀번호는 최소 8자리 이상이어야 합니다.'})

    if (
        re.search("[a-z]+", password) is None or re.search("[A-Z]+", password) is None
    ):
        raise ApiException({'error_message': '비밀번호는 최소 1개 이상의 영문 대소문자가 포함되어야 합니다.'})

    if re.search("[0-9]+", password) is None:
        raise ApiException({'error_message': '비밀번호는 최소 1개 이상의 숫자가 포함되어야 합니다.'})

    if not any(sc in Constants.SPECIAL_CHARACTERS for sc in password):
        raise ApiException({'error_message': '비밀번호는 최소 1개 이상의 특수문자가 포함되어야 합니다.'})

    return True


def find_password(request_json: Dict) -> Dict:
    """비밀번호 찾기 (재설정)

    SMS 인증에 성공한 Request id를 검증 후 새로운 비밀번호 발급 혹은 변경 링크를 제공한다.

    Args:
        request_json(Dict): 회원 가입 요청 body 값

    """
    try:
        # 요청 파라미터 validation
        reg_params = FindPasswordSchema().load(request_json)

        # 회원 가입 파라미터
        email = reg_params.get('email')
        request_id = reg_params.get('request_id')
        mobile_num = reg_params.get('mobile_num')

        with session_scope() as loc_session:
            # Request ID 사용 처리
            sms_type = Constants.SMS_TYPE_PASSWORD
            UserSmsRequest.use_request(loc_session, sms_type, request_id, mobile_num)

            # 회원 체크
            User.check_user(loc_session, email, mobile_num)

            # 임시 패스워드 제공 및 이메일로 변경 링크 제공
            print('[FindPassword] Email & SMS 비밀번호 초기화 링크 전달')
        return {'result': 'success'}
    except ValidationError as ex:
        return abort(400, 'Validation Error', **v_msg(ex.messages))
    except ApiException as ex:
        return abort(ex.code, ex.message, **ex.to_json())
    except BaseException as ex:
        details = template.format(type(ex).__name__, ex.args)
        return abort(500, '비밀번호 찾기 중 오류가 발생하였습니다.', details=details)
