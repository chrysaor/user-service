from flask_restx import Namespace, fields


class UserDto:
    """
    회원 관리 Data
    """
    api = Namespace("user", description="사용자 관리")

    user_info = api.model(
        "user_info",
        {
            "email": fields.String(
                required=True,
                description="사용자 로그인 아이디",
                example="son@softbank.com",
                attribute="email"
            ),
            "name": fields.String(
                required=False,
                description="회원 이름",
                example="손정의",
                attribute="name"
            ),
            "nickname": fields.String(
                required=False,
                description="회원 닉네임",
                example="Masayoshi_Son",
                attribute="nickname"
            ),
            "mobile_num": fields.String(
                required=True,
                description="휴대폰 번호",
                example="01021990054",
                attribute="mobile_num"
            ),
        },
    )

    register_sms_req = api.inherit(
        "register_sms_req",
        user_info,
        {
            "sms_type": fields.String(
                required=True,
                description="SMS 인증 요청 타입, (REGISTER, LOGIN, FIND_PASSWORD)",
                example="REGISTER",
                attribute="sms_type",
            ),
        }
    )

    register_user = api.inherit(
        "register_user",
        user_info,
        {
            "password": fields.String(
                required=True,
                description="회원 비밀번호",
                example="12345678",
                attribute="password"
            ),
            "request_id": fields.String(
                required=True,
                description="SMS 인증 완료된 request id",
                example="685d4dfc5e8519f11bdc9b82870bc4a2a073d558",
                attribute="request_id"
            ),
        }
    )
