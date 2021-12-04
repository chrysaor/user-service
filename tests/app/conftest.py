import os
from os.path import isfile

import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config.base import TestDBConfig
from app.database.models import Base


# @pytest.fixture(scope='session')
# def flask_app():
#     app = create_app()
#     app_context = app.app_context()
#     app_context.push()
#
#     yield app
#
#     app_context.pop()


# @pytest.fixture(scope='session')
# def flask_client(flask_app):
#     return flask_app.test_client()


@pytest.fixture(scope='session')
def db():
    db_url = TestDBConfig.db_uri()
    engine = create_engine(db_url, echo=False)
    session = sessionmaker(bind=engine)
    fixture_db = {
        'engine': engine,
        'session': session
    }
    Base.metadata.create_all(bind=engine, checkfirst=True)

    yield fixture_db

    engine.dispose()

    # DB file delete
    if isfile('test.db'):
        os.remove('test.db')


@pytest.fixture(scope='function')
def session(db):
    session = db['session']()

    yield session

    session.rollback()
    session.close()
