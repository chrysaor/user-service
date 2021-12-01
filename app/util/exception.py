from typing import Dict


def v_msg(error_message: str):
    return {
        'error_code': 'VALIDATION_EXCEPTION',
        'error_message': error_message
    }


class ApiException(Exception):
    code = 400
    message = 'Bad request'
    error_code = 'API_BASE_EXCEPTION'
    error_message = 'API 호출 중 오류가 발생하였습니다.'

    def __init__(self, resource: Dict):
        if 'error_code' in resource:
            self.error_code = resource.get('error_code')
        if 'error_message' in resource:
            self.error_message = resource.get('error_message')

    def to_json(self):
        return {
            'error_code': self.error_code, 'error_message': self.error_message,
        }
