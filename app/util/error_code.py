class AuthError:
    UserNotFound = {
        'error_code': 'LOGIN_ERROR',
        'error_message': '사용자 정보 조회 중 오류가 발생하였습니다.'
    }

    PasswordError = {
        'error_code': 'INVALID_PASSWORD_OR_ID',
        'error_message': '비밀번호 혹은 아이디가 올바르지 않습니다.'
    }

    SmsAuthError = {
        'error_code': 'SMS_AUTH_ERROR',
        'error_message': 'SMS 인증번호가 올바르지 않거나 시간이 초과되었습니다.'
    }

    RequestAlreadyUsed = {
        'error_code': 'SMS_ALREADY_COMPLETE',
        'error_message': '이미 사용 완료된 요청 입니다.'
    }

    UserAlreadyRegistered = {
        'error_code': 'USER_ALREADY_REGISTERED',
        'error_message': '이미 가입된 회원입니다.'
    }


class TokenError:
    TokenExpired = {
        'error_code': 'TOKEN_EXPIRED',
        'error_message': '이미 만료된 토큰입니다.'
    }

    InvalidToken = {
        'error_code': 'INVALID_TOKEN',
        'error_message': '올바르지 않은 토큰입니다.'
    }


class ApiError:
    ResourceNotFound = {
        'error_code': 'RESOURCE_IS_NOT_FOUND',
        'error_message': '해당하는 리소스가 없습니다.'
    }

    BadRequest = {
        'error_code': 'BAD_REQUEST',
        'error_message': '잘못된 요청입니다.'
    }
