from app.util.exception import v_msg


def test_v_msg():
    """Validation Exception Message 테스트"""
    message = v_msg('test_message')

    assert(message.get('error_code') == 'VALIDATION_EXCEPTION')
    assert(message.get('error_message') == 'test_message')

    message = v_msg('')
    assert(message.get('error_code') == 'VALIDATION_EXCEPTION')
    assert(message.get('error_message') == '')
