from flask_restx import abort


def get_health_check():
    """
    Health check 결과 조회
    """
    try:
        return {"health_check": True}
    except BaseException as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = "Health check 결과 조회 중 오류가 발생하였습니다."
        details = template.format(type(ex).__name__, ex.args)
        return abort(500, message, details=details)
