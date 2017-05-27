"""
Tests related to get lists of stuffs.
"""

def test_can_get_bibliographies(client):
    _, res = client.get('/bibliography')
    assert res.status == 200


def test_can_get_documents(client):
    _, res = client.get('/document?bibliography=123')
    assert res.status == 200
    assert res.json() == []


def test_get_documents_require_bibliography(client):
    _, res = client.get('/document')
    assert res.status == 400
    assert 'error' in res.json()


def test_can_get_matrices(client):
    _, res = client.get('/matrix')
    assert res.status == 200
    assert res.json() == []


def test_can_get_ranking_matrices(client):
    _, res = client.get('/ranking')
    assert res.status == 200
    assert res.json() == []
