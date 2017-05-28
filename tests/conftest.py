import json
import pytest
import os

from condor.config import DEFAULT_DB_PATH
from condor.models.base import DeclarativeBase
from sanic.testing import SanicTestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


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
    return _engine


@pytest.fixture()
def session(engine):
    """
    Creates a session maker instance attached to our default engine.
    """
    _session = scoped_session(sessionmaker(bind=engine))
    yield _session
    _session.rollback()


@pytest.fixture(autouse=True)
def fresh_database(session, monkeypatch):
    """
    Use a fresh database everytime tests run.
    """
    def mock_requires_db(func):
        def wrapper(*args, **kwargs):
            db = session()
            monkeypatch.setattr(db, 'commit', db.flush)
            return func(db, *args, **kwargs)
        return wrapper
    monkeypatch.setattr('condor.dbutil.requires_db', mock_requires_db)
