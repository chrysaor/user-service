from flask_restx import Namespace, fields


class AuthDto:
    """
    인증 관리 DTO

    flask_restx -> Namespace 및 Swagger Document의 Model을 정의한다.
    """
    api = Namespace("auth", description="인증 관리")
    input_login = api.model(
        "input_login",
        {
            "id": fields.String(required=True, description="사용자 아이디 혹은 휴대폰 번호"),
            "password": fields.String(required=True, description="사용자 비밀번호"),
        },
    )

    output_login = api.model(
        "output_login",
        {
            "access_token": fields.String(
                description="인증 토큰", example="eyJ0...", attribute="access_token"
            ),
            "name": fields.String(
                default="이름",
                description="회원 이름",
                attribute="name",
            ),
            "nickname": fields.String(
                default="닉네임",
                description="회원 닉네임",
                attribute="nickname",
            ),
            "email": fields.String(
                example="chrysaor@naver.com",
                description="전자우편",
                attribute="email",
            ),
        },
    )

    success = api.model(
        "success",
        {
            "result": fields.String(
                example="success",
                attribute="result",
            ),
        },
    )

    password_reset = api.model(
        "password_reset",
        {
            "request_id": fields.String(
                required=True,
                description="SMS 인증 요청시 발급받은 ID",
                example="Aujq2docQlCpqiD28Fz",
                attribute="request_id"
            ),
            "email": fields.String(
                example="chrysaor@naver.com",
                description="전자우편",
                attribute="email",
            ),
            "mobile_num": fields.String(
                example="chrysaor@naver.com",
                description="전자우편",
                attribute="email",
            ),
        }
    )
