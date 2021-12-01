from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from app.config.base import DBConfig

database_engine = create_engine(
    DBConfig.db_uri(),
    encoding="UTF-8",
    pool_size=20,
    max_overflow=0,
)

# Session
Session = sessionmaker(bind=database_engine)

# Scoped session
session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=database_engine)
)

Base = declarative_base()
Base.query = session.query_property()


def init_db():
    # 모델 분리를 위한 import
    from app.model.user import user, user_sms_request

    # Import model 출력
    print('=' * 80)
    print('[Initiate DB]')
    print('-' * 80)
    print(user.User.__tablename__)
    print(user_sms_request.UserSmsRequest.__tablename__)
    print('=' * 80)

    # Create database
    try:
        Base.metadata.create_all(bind=database_engine, checkfirst=True)
    except BaseException as ex:
        print(ex)


@contextmanager
def session_scope():
    """트랜잭션 처리용 context manager 패턴"""
    with_session = Session()
    try:
        yield with_session
        with_session.commit()
    except BaseException:
        with_session.rollback()
        raise
    finally:
        with_session.close()
