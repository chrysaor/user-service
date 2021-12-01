import json
from typing import Dict

from flask_restx import abort
from marshmallow import ValidationError

from app.database.models import session, session_scope
from app.model.user.user import User
from app.model.user.user_sms_request import UserSmsRequest
from app.schema.user.user_registration_schema import UserRegistrationSchema, UserInfoSchema
from app.util.constants import template, Constants
from app.util.exception import ApiException, v_msg


def create_user(request_json: Dict) -> Dict:
    """회원 가입

    발급된 SMS 인증번호와 Request ID를 받아 회원 가입을 완료한다.

    Args:
        request_json(Dict): 회원 가입 요청 body 값

    Returns:
        Dict: 회원 가입 정보

    """
    try:
        # 요청 파라미터 validation
        reg_params = UserRegistrationSchema().load(request_json)

        # 회원 가입 파라미터
        email = reg_params.get('email')
        password = reg_params.get('password')
        request_id = reg_params.get('request_id')
        mobile_num = reg_params.get('mobile_num')
        del reg_params['request_id']
        del reg_params['password']

        with session_scope() as loc_session:
            # Request ID 사용 처리
            sms_type = Constants.SMS_TYPE_REG
            UserSmsRequest.use_request(loc_session, sms_type, request_id, mobile_num)

            # 기가입 체크 - 이메일 번호, 휴대폰 번호
            User.is_already_registered(loc_session, email, mobile_num)

            # 회원 가입
            user_instance = User.user_registration(loc_session, reg_params, password)

            # Make result data
            user_data = UserInfoSchema().dumps(user_instance)

        return json.loads(user_data)
    except ValidationError as ex:
        return abort(400, 'Validation Error', **v_msg(ex.messages))
    except ApiException as ex:
        return abort(ex.code, ex.message, **ex.to_json())
    except BaseException as ex:
        details = template.format(type(ex).__name__, ex.args)
        return abort(500, '회원 가입 중 오류가 발생하였습니다.', details=details)


def get_a_user(user_id):
    """
    특정 사용자 상세 조회
    """
    try:
        return session.query(User).filter(User.id == user_id).first()
    except Exception as ex:
        details = template.format(type(ex).__name__, ex.args)
        return abort(500, '사용자 상세 조회 중 오류가 발생하였습니다.', details=details)
    finally:
        session.close()
