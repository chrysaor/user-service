from datetime import datetime
from typing import Dict

import bcrypt

from sqlalchemy import Column, String, DateTime, BigInteger, Boolean
from sqlalchemy.orm import Session

from app.database.models import Base
from app.util.error_code import AuthError
from app.util.exception import ApiException


class User(Base):
    """
    회원 정보 테이블
    """
    __tablename__ = "user"

    id = Column("id", BigInteger, primary_key=True, autoincrement=True)
    email = Column("email", String(320), index=True, unique=True)
    password = Column("password", String)
    name = Column("name", String(20), index=True)
    nickname = Column("nickname", String(20), index=True)
    mobile_num = Column("mobile_num", String(20), index=True, unique=True)
    mobile_verification = Column("mobile_verification", Boolean, default=False)
    registration_date = Column("registration_date", DateTime)
    personal_id = Column("personal_id", String, default='')
    authority = Column("authority", String, default='NORMAL')
    access_token = Column("access_token", String, index=True)
    created_at = Column("created_at", DateTime(timezone=False))
    is_deleted = Column("is_deleted", Boolean)
    deleted_at = Column("deleted_at", DateTime(timezone=False))
    deleted_by = Column("deleted_by", String)

    @classmethod
    def get_password(cls, password: str) -> str:
        """패스워드 생성 함수

        bcrypt 라이브러리를 이용하여 패스워드 생성, 솔트값은 램덤하게 생성

        Args:
            password (str): 패스워드 문자열

        """
        encrypted_password = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        )

        # 데이터 베이스 저장을 위해 bytes 객체를 utf-8로 디코딩하여 str 객체로 변환
        return encrypted_password.decode("utf-8")

    def check_password(self, password: str) -> bool:
        """비밀번호 체크 함수

        Args:
            password (str): 사용자 패스워드 스트링

        Returns:
            bool: 동일한 패스워드면 True, 아닐 경우 False

        """
        return bcrypt.checkpw(
            password.encode("utf-8"), self.password.encode("utf-8")
        )

    @classmethod
    def is_already_registered(cls, session: Session, email: str, mobile: str):
        """기가입 체크 로직

        Args:
            session(Session): sqlalchemy 세션
            email(str): 이메일
            mobile(str): 휴대폰 번호

        Raises:
            ApiException: 이미 사용중인 계정인 경우 발생
        """
        user_instance = session.query(User).filter(
            User.email == email
        ).first()

        # 이미 사용중인 계정인 경우
        if user_instance is not None:
            raise ApiException(AuthError.UserAlreadyRegistered)

        user_instance = session.query(User).filter(
            User.email != email,
            User.mobile_num == mobile,
        ).first()

        # 다른 이메일 계정에 등록되어 있는 경우 해당 계정 인증 해제
        if user_instance is not None:
            user_instance.mobile_num = ''
            user_instance.mobile_verification = False

    @classmethod
    def user_registration(cls, session: Session, params: Dict, password: str):
        """회원 등록

        Args:
            session(Session): sqlalchemy 세션
            params(Dict): 회원 등록 파라미터
            password(str): 패스워드

        Returns:
            User: User 인스턴스
        """
        user_instance = User(
            email=params.get('email'),
            password=User.get_password(password),
            name=params.get('name'),
            nickname=params.get('nickname'),
            mobile_num=params.get('mobile_num'),
            mobile_verification=True,
            created_at=datetime.today()
        )

        session.add(user_instance)

        return user_instance

    @classmethod
    def get_user_by_id(cls, session: Session, user_id: int = None):
        """회원 ID를 통한 회원 조회

        Args:
            session(Session): Sqlalchemy 세션
            user_id(int): 회원 아이디

        Returns:
            User: 회원 인스턴스

        """
        user_instance = session.query(User).filter(
            User.id == user_id
        ).first()

        if user_instance is None:
            raise ApiException(AuthError.UserNotFound)

        return user_instance

    @classmethod
    def check_user(cls, session: Session, email: str, mobile_num: str):
        """이메일, 휴대폰 번호로 회원 여부 체크

        Args:
            session(Session): Sqlalchemy 세션
            email(str): 회원 이메일
            mobile_num(str): 회원 휴대폰 번호

        """
        user_instance = session.query(User).filter(
            User.email == email,
            User.mobile_num == mobile_num,
        ).first()

        if user_instance is None:
            raise ApiException(AuthError.UserNotFound)

    @classmethod
    def clear_token(cls, session: Session, user_id: int, token: str):
        """인증 토큰 초기화

        Args:
            session(Session): sqlalchemy 세션
            user_id(int): 회원 아이디
            token(str): 인증 토큰

        Raises:
            ApiException: 토큰 혹은 회원이 없는 경우 발생

        """
        user_instance = session.query(User).filter(
            User.id == user_id,
            User.access_token == token
        ).first()

        if user_instance is None:
            raise ApiException(AuthError.UserNotFound)

        user_instance.access_token = None
