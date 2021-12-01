from app.util.common import check_email


def check_email_test():
    assert(check_email('chrysaor@naver.com') is True)
