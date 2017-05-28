import json
import os
from unittest import mock

import pytest

from condor.config import DEFAULT_DB_PATH
from condor.models.base import DeclarativeBase
from sanic.testing import SanicTestClient
from sqlalchemy import create_engine
from sqlalchemy.orm.session import Session


class DecoratedResponse(object):
    def __init__(self, response):
        self._response = response
    def json(self):
        return json.loads(self._response.body.decode('utf-8'))
    def __getattr__(self, name):
        return getattr(self._response, name)


class WrappedSanicTestClient(SanicTestClient):
    def _sanic_endpoint_test(self, *args, **kwargs):
        req, res = super()._sanic_endpoint_test(*args, **kwargs)
        return req, DecoratedResponse(res)



@pytest.fixture()
def client():
    """
    A simple test client wrapper.
    """
    from app import app
    return WrappedSanicTestClient(app)


@pytest.fixture(scope='session')
def engine():
    """
    Creates an engine to handle our database.
    """
    # Use a sqlite database by default.
    default_url = 'sqlite:///' + os.path.join(DEFAULT_DB_PATH, 'condor.db.test')
    _engine = create_engine(default_url)
    DeclarativeBase.metadata.drop_all(_engine)
    DeclarativeBase.metadata.create_all(_engine)
    yield _engine
    _engine.dispose()


@pytest.fixture(scope='function')
def connection(engine):
    _connection = engine.connect()
    yield _connection
    _connection.close()


@pytest.fixture(scope='function')
def transaction(connection):
    _transaction = connection.begin()
    yield _transaction
    _transaction.rollback()


@pytest.fixture(scope='function')
def session(connection, transaction, monkeypatch):
    _session = Session(connection, autocommit=False)
    # Make sure we do not commit
    monkeypatch.setattr(_session, 'commit', _session.flush)
    yield _session
    _session.close()


@pytest.fixture(scope='function', autouse=True)
def fresh_database(session, monkeypatch):
    """
    Use a fresh database everytime tests run.
    """
    def requires_db_mock(func):
        def wrapper(*args, **kwargs):
            # assert False, 'Here'
            return func(session, *args, **kwargs)
        return wrapper
    monkeypatch.setattr('app.requires_db', requires_db_mock)
