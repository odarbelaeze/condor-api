"""
Tests of simple concepts.
"""

import pytest


def test_one_equals_one():
    assert 1 == 1


@pytest.mark.xfail
def test_one_equals_two():
    assert 1 == 2


def test_ping(client):
    res = client.get('/ping')
    assert res.status_code == 200
    assert res.text == 'pong'
