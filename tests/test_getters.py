"""
Tests related to get lists of stuffs.
"""


import pytest

from app import app


@pytest.fixture()
def client():
    return app.test_client


def test_can_get_bibliographies(client):
    _, res = client.get('/bibliography')
    assert res.status == 200


async def test_can_get_documents(client):
    _, res = client.get('/document?bibliography=123')
    assert res.status == 200
    assert await res.json() == "[]"
