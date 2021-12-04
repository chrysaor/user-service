import os
from datetime import datetime, timedelta


class DBConfig:
    db_uri_str = None

    @classmethod
    def db_uri(cls):
        db_type = os.environ.get("DB_TYPE", "postgresql")
        db_user = os.environ.get("DB_USER", "postgres")
        db_password = os.environ.get("DB_PASSWORD", "1q2w3e4r")
        db_hostname = os.environ.get("DB_HOSTNAME", "127.0.0.1")
        db_port = os.environ.get("DB_PORT", 5432)
        db_name = os.environ.get("DB_NAME", "postgres")

        cls.db_uri_str = f"{db_type}://{db_user}:{db_password}@{db_hostname}:{db_port}/{db_name}"
        return cls.db_uri_str


class TestDBConfig(DBConfig):
    @classmethod
    def db_uri(cls):
        return 'sqlite:///tests/app/test.db'


class Config:
    APPLICATION_NAME = 'user-service'
    CONFIG_NAME = 'base'

    # SQLAlchemy 설정
    SQLALCHEMY_DATABASE_URI = DBConfig.db_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_POOL_SIZE = 30

    # 인증 관련 설정
    JWT_TOKEN_EXP = datetime.utcnow() + timedelta(minutes=30)


class DevelopmentConfig(Config):
    APPLICATION_NAME = 'user-service'
    CONFIG_NAME = 'development'

    # Flask 설정
    DEBUG = True

    # SQLAlchemy 설정
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_POOL_SIZE = 30


class ProductionConfig(Config):
    APPLICATION_NAME = 'user-service'
    CONFIG_NAME = 'production'

    # Flask 설정
    DEBUG = False

    # SQLAlchemy 설정
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_POOL_SIZE = 30

    # Swagger 문서 등록 해제
    RESTX_MASK_SWAGGER = False


config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
