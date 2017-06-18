import json
import os
from unittest import mock

import pytest

from condor.config import DEFAULT_DB_PATH
from condor.models.base import DeclarativeBase
from apistar.test import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm.session import Session



@pytest.fixture(scope='session')
def engine():
    """
    Creates an engine to handle our database.
    """
    # Use a sqlite database by default.
    default_url = 'sqlite:///' + os.path.join(DEFAULT_DB_PATH, 'condor.db.test')
    _engine = create_engine(default_url, isolation_level='READ_UNCOMMITTED')
    DeclarativeBase.metadata.drop_all(_engine)
    DeclarativeBase.metadata.create_all(_engine)
    yield _engine
    _engine.dispose()


@pytest.fixture(scope='session')
def connection(engine):
    _connection = engine.connect()
    yield _connection
    _connection.close()


@pytest.fixture(scope='session')
def transaction(connection):
    _transaction = connection.begin()
    yield _transaction
    _transaction.rollback()


@pytest.fixture(scope='function')
def session(connection, transaction, monkeypatch):
    _transaction = connection.begin_nested()
    _session = Session(connection, autoflush=False, autocommit=False)
    # Make sure we do not commit
    monkeypatch.setattr(_session, 'commit', _session.flush)
    yield _session
    _session.close()
    _transaction.rollback()


@pytest.fixture(scope='function', autouse=True)
def fresh_database(session, monkeypatch):
    """
    Use a fresh database everytime tests run.
    """
    monkeypatch.setattr('condor.dbutil.session', lambda: session)


@pytest.fixture()
def client():
    """
    A simple test client wrapper.
    """
    return TestClient()
