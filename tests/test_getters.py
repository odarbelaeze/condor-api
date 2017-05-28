"""
Tests related to get lists of stuffs.
"""

from condor.models import Document, Bibliography


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


def test_document_endpoint_actually_returns_documents(client, session):
    # Given some records matching records in the database
    bib = Bibliography(eid='123', description='lorem')
    session.add(bib)
    session.flush()
    doc = Document(
        eid='345',
        bibliography_eid='123',
        title='lorem',
        keywords='{}',
        description='lorem',
        language='english',
        hash='alksdjksjdf'
    )
    session.add(doc)
    session.commit()
    # When I request the documents with the given bibliography eid
    _, res = client.get('/document?bibliography=123')
    # Then I receive a successful response
    assert res.status == 200
    # And the response is non empty
    assert len(res.json()) > 0