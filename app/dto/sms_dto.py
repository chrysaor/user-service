from flask_restx import Namespace, fields


class SmsDto:
    """
    SMS 인증 요청 Data
    """
    api = Namespace("sms", description="SMS 관리")

    validation_req = api.model(
        "sms_validation_req",
        {
            "sms_type": fields.String(
                required=True,
                description="SMS 인증 요청 타입 ['REGISTER', 'LOGIN', 'FIND_PASSWORD']",
                example="Aujq2docQlCpqiD28Fz",
                attribute="sms_type"
            ),
            "request_id": fields.String(
                required=True,
                description="SMS 인증 요청시 발급받은 ID",
                example="Aujq2docQlCpqiD28Fz",
                attribute="request_id"
            ),
            "mobile_num": fields.String(
                required=True,
                description="회원 휴대폰 번호",
                example="01021990054",
                attribute="mobile_num"
            ),
            "auth_code": fields.String(
                required=True,
                description="발급받은 6자리 SMS 인증 코드",
                example="283751",
                attribute="auth_code"
            ),
        }
    )
