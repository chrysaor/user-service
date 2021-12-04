from app.util.constants import template, Constants


def test_template():
    """템플릿 메시지 테스트"""
    assert template == 'An exception of type {0} occurred. Arguments:\n{1!r}'


def test_constants():
    """Constant 테스트"""
    # Response
    assert(len(Constants.RESPONSES) == 6)
    assert(Constants.RESPONSES.get(200) == 'Success')
    assert(Constants.RESPONSES.get(400) == 'Bad Request')
    assert(Constants.RESPONSES.get(401) == 'Unauthorized resources has been accessed')
    assert(Constants.RESPONSES.get(403) == 'Authenticated clients access unauthorized resources')
    assert(Constants.RESPONSES.get(404) == 'Resource Not Found')
    assert(Constants.RESPONSES.get(500) == 'Internal Server Error')

    # Special character
    assert(Constants.SPECIAL_CHARACTERS == ' !\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~')

    # SMS constants
    assert(Constants.SMS_TYPE_REG == 'REGISTER')
    assert(Constants.SMS_TYPE_PASSWORD == 'FIND_PASSWORD')
    assert(Constants.SMS_TYPE_LOGIN == 'LOGIN')
