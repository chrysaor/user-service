from datetime import datetime
from dateutil.relativedelta import relativedelta

from sqlalchemy import Column, String, DateTime, BigInteger, Boolean, Integer
from sqlalchemy.orm import Session

from app.database.models import Base
from app.util.error_code import ApiError, AuthError
from app.util.exception import ApiException


class UserSmsRequest(Base):
    """
    SMS 인증 문자 발송 처리 테이블
    """
    __tablename__ = "user_sms_request"

    id = Column("id", BigInteger, primary_key=True, autoincrement=True)
    user_id = Column("user_id", BigInteger, index=True)
    request_id = Column("request_id", String)  # 고유 request id
    auth_code = Column("auth_code", String)  # 인증코드 형식: 317284
    sms_type = Column("sms_type", String(20))  # MOBILE_LOGIN, FIND_PASSWORD
    mobile_num = Column("mobile_num", String(20), index=True)  # SMS 인증 요청 번호
    request_count = Column("request_count", Integer, default=0)  # SMS 인증번호 입력 제한 횟수
    limit_count = Column("limit_count", Integer, default=3)  # SMS 인증번호 입력 제한 횟수
    is_completed = Column("is_completed", Boolean, default=False)  # 인증 완료 여부
    completed_at = Column("completed_at", DateTime(timezone=False))  # 인증 완료 시간
    is_used = Column("is_used", Boolean, default=False)  # 인증 완료 후 사용 여부
    used_at = Column("used_at", DateTime(timezone=False))  # 사용 일시
    created_at = Column("created_at", DateTime(timezone=False))  # 요청 일시

    @classmethod
    def create(cls, session: Session, params: dict):
        """UserSmsRequest 생성

        Args:
            session(Session): sqlalchemy session
            params(dict): UserSmsRequest parameter

        Returns:

        """
        user_sms_request = UserSmsRequest(**params)

        session.add(user_sms_request)
        session.commit()

        return user_sms_request

    @classmethod
    def complete_sms_auth(cls, session: Session, sms_type: str, request_id: str,
                          mobile_num: str, auth_code: str, user_id: int = None):
        """SMS 인증 완료

        Args:
            session(Session): sqlalchemy 세션
            sms_type(str): SMS 인증 타입
            request_id(str): 요청 ID
            mobile_num(str): 휴대폰 번호
            auth_code(str): 인증 코드 - 6자리 숫자
            user_id(int): 유저 ID. 선택적 필드

        Raise:
            SmsAuthErrorException: 인증 시간이 지났거나 (5분), 코드가 맞지 않는 경우 발생

        """
        # 5분 이내의 발급된 코드만 인정
        current = datetime.utcnow()
        before_time = current - relativedelta(minutes=10)

        sms_req_query = session.query(UserSmsRequest).filter(
            UserSmsRequest.sms_type == sms_type,
            UserSmsRequest.request_id == request_id,
            UserSmsRequest.mobile_num == mobile_num,
            UserSmsRequest.request_count < UserSmsRequest.limit_count,
            UserSmsRequest.is_completed.is_(False),
            UserSmsRequest.created_at >= before_time,
        )

        if user_id is not None:
            sms_req_query = sms_req_query.filter(UserSmsRequest.user_id == user_id)

        # 타겟 가져오기
        sms_request = sms_req_query.first()

        # 유효한 요청이 없는 경우
        if sms_request is None:
            raise ApiException(AuthError.SmsAuthError)

        # 인증 코드가 틀린 경우
        if sms_request.auth_code != auth_code:
            sms_request.request_count += 1
            session.commit()
            raise ApiException(AuthError.SmsAuthError)

        # 인증 코드 일치
        sms_request.is_completed = True
        sms_request.completed_at = current

    @classmethod
    def use_request(cls, session: Session, sms_type: str, request_id: str,
                    mobile_num: str, user_id: int = None):
        """Request ID 완료 처리

        Args:
            session(Session): sqlalchemy
            sms_type(str): SMS 인증 요구 타입
            request_id(str): Request ID
            mobile_num(str): 휴대폰 번호
            user_id(str): 회원 아이디 (Optional)

        Raises:
            BadRequestException: 해당하는 조건에 해당하는 인스턴스가 없는 경우 발생
            RequestAlreadyUsed: 이미 사용된 요청인 경우 발생

        """
        req_query = session.query(UserSmsRequest).filter(
            UserSmsRequest.sms_type == sms_type,
            UserSmsRequest.request_id == request_id,
            UserSmsRequest.mobile_num == mobile_num,
        )

        if user_id is not None:
            req_query = req_query.filter(UserSmsRequest.user_id == user_id)

        # UserSmsRequest 인스턴스 가져오기
        req_instance = req_query.first()

        if req_instance is None:
            raise ApiException(ApiError.BadRequest)

        if req_instance.is_used:
            raise ApiException(AuthError.RequestAlreadyUsed)

        current = datetime.now()
        req_instance.is_used = True
        req_instance.used_at = current
