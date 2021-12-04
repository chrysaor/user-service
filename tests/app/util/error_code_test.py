from app.util.error_code import AuthError, TokenError, ApiError


def key_check(error_obj):
    """error_code & error_message 테스트"""
    if 'error_code' not in error_obj:
        return False

    if 'error_message' not in error_obj:
        return False

    return True


def test_auth_error():
    """인증 오류 메시지 테스트"""
    assert(AuthError.SmsAuthError is not None)
    assert(key_check(AuthError.SmsAuthError) is True)

    assert(AuthError.PasswordError is not None)
    assert(key_check(AuthError.PasswordError) is True)

    assert(AuthError.UserNotFound is not None)
    assert(key_check(AuthError.UserNotFound) is True)

    assert(AuthError.RequestAlreadyUsed is not None)
    assert(key_check(AuthError.RequestAlreadyUsed) is True)

    assert(AuthError.UserAlreadyRegistered is not None)
    assert(key_check(AuthError.UserAlreadyRegistered) is True)


def test_token_error():
    """토큰 에러 메시지 테스트"""
    assert(TokenError.TokenExpired is not None)
    assert(key_check(TokenError.TokenExpired) is True)

    assert(TokenError.InvalidToken is not None)
    assert(key_check(TokenError.InvalidToken) is True)


def test_api_error():
    """API 에러 메시지 테스트"""
    assert(ApiError.ResourceNotFound is not None)
    assert(key_check(ApiError.ResourceNotFound) is True)

    assert(ApiError.BadRequest is not None)
    assert(key_check(ApiError.ResourceNotFound) is True)
