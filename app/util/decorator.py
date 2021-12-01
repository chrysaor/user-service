import time

from functools import wraps
from typing import Callable
from flask import request, g
from flask_restx import abort

from app.service.auth_service import decode_auth_token
from app.util.constants import template
from app.util.exception import ApiException


def elapsed_time(original_func) -> Callable:
    """함수 실행시간 측정 데코레이터"""
    @wraps(original_func)
    def wrapper(*args, **kwargs):
        start = time.time()
        original_func(*args, **kwargs)
        end = time.time()
        print("함수 수행시간: %f 초" % (end - start))

    return wrapper


def token_required(original_func: Callable) -> Callable:
    """사용자 토큰 확인 데코레이터"""
    @wraps(original_func)
    def wrapper(*args, **kwargs):
        try:
            resp = decode_auth_token(request)
        except ApiException as ex:
            return abort(401, ex.message, **ex.to_json())
        except BaseException as ex:
            details = template.format(type(ex).__name__, ex.args)
            return abort(400, '로그인 중 오류가 발생하였습니다.', details=details)

        # Save token to flask global context
        g.user_token = resp.get('access_token')
        g.user_id = resp.get('user_id')

        return original_func(*args, **kwargs)

    return wrapper


def admin_token_required(original_func: Callable) -> Callable:
    """관리자 토큰 확인 데코레이터"""
    @wraps(original_func)
    def wrapper(*args, **kwargs):
        # 계정 권한 정보 확인용 - 미사용
        authority = g.get('authority')
        if authority != 'admin':
            return abort(403, '권한이 없습니다.', details='')

        return original_func(*args, **kwargs)

    return wrapper
