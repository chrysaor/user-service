import random
from datetime import datetime
from typing import Dict

from flask_restx import abort
from marshmallow import ValidationError

from app.database.models import session, session_scope
from app.model.user.user_sms_request import UserSmsRequest
from app.schema.sms.sms_request_schema import SmsRequestSchema
from app.schema.sms.sms_validation_schema import SmsValidationSchema
from app.util.common import make_request_id
from app.util.constants import template
from app.util.exception import ApiException, v_msg


def sms_request(request_json: Dict) -> Dict:
    """SMS 인증 요청

    이메일, 이름, 닉네임, 모바일 번호를 입력받아 SMS 인증을 요청한다.
    인증 요청이 도착하면 유효성 검사 후 요청 아이디를 발급하여 부여한다.
    작업이 종료되면 SMS 요청 서비스에 발송 요청 (가정)

    Args:
        request_json(dict): SMS 인증요청 body 값
    Returns:
        dict: SMS 인증 요청 응답 값
    """
    try:
        # 요청 파라미터 validation
        sms_req = SmsRequestSchema().load(request_json)

        # 파라미터들
        sms_type = sms_req.get('sms_type')
        email = sms_req.get('email')
        name = sms_req.get('name', '')
        nickname = sms_req.get('nickname', '')
        mobile_num = sms_req.get('mobile_num')

        # Request id & 인증 코드 생성
        today = datetime.now()
        request_id = make_request_id(
            email, name, nickname, mobile_num, str(today.timestamp())
        )
        auth_code = ''.join(random.choice('0123456789') for _ in range(6))

        # SMS 인증 요청 정보 저장
        UserSmsRequest.create(session, dict(
            request_id=request_id,
            auth_code=auth_code,
            sms_type=sms_type,
            mobile_num=mobile_num,
            request_count=0,
            limit_count=3,
            created_at=today,
        ))

        # 구현 필요 부분: SMS 전송 요청
        # 외부 시스템 연동 혹은 메시지 전송
        return {'request_id': request_id}
    except ValidationError as ex:
        return abort(400, 'Validation Error', **v_msg(ex.messages))
    except ApiException as ex:
        return abort(ex.code, ex.message, **ex.to_json())
    except BaseException as ex:
        message = "SMS 발송 요청중 오류가 발생하였습니다."
        details = template.format(type(ex).__name__, ex.args)
        return abort(500, message, details=details)


def sms_request_validation(request_json: dict) -> Dict:
    """SMS 인증 완료

    발급된 SMS 인증번호와 Request ID를 받아 인증을 완료한다.

    Args:
        request_json(dict): SMS 인증 완료 요청 body 값

    Returns:
        dict: SMS 인증 요청 응답 값

    """
    try:
        # 요청 파라미터 validation
        validation_req = SmsValidationSchema().load(request_json)

        # 파라미터들
        sms_type = validation_req.get('sms_type')
        request_id = validation_req.get('request_id')
        mobile_num = validation_req.get('mobile_num')
        auth_code = validation_req.get('auth_code')

        # SMS 인증 완료 처리
        with session_scope() as loc_session:
            UserSmsRequest.complete_sms_auth(
                loc_session, sms_type, request_id, mobile_num, auth_code
            )

        return {
            'sms_type': sms_type,
            'request_id': request_id,
            'mobile_num': mobile_num,
        }
    except ValidationError as ex:
        return abort(400, 'Validation Error', **v_msg(ex.messages))
    except ApiException as ex:
        return abort(ex.code, ex.message, **ex.to_json())
    except BaseException as ex:
        message = "SMS 발송 요청중 오류가 발생하였습니다."
        details = template.format(type(ex).__name__, ex.args)
        return abort(500, message, details=details)
