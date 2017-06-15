"""
Tests related to get lists of stuffs.
"""

from condor.models import Document, Bibliography, TermDocumentMatrix, \
    RankingMatrix


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

def test_matrix_endpoint_when_there_are_matrix(client, session):
    # Given some records matching records in the database
    bib = Bibliography(eid='123', description='lorem')
    session.add(bib)
    session.flush()
    mat = TermDocumentMatrix(
        eid='345',
        bibliography_eid='123',
        bibliography_options='',
        processing_options='',
        term_list_path='',
        matrix_path='',
    )
    session.add(mat)
    session.commit()
    # When I request the documents with the given bibliography eid
    _, res = client.get('/matrix')
    # Then I receive a successful response
    assert res.status == 200
    # The response is non empty
    assert len(res.json()) == 1
    # And has matrix
    assert any(m.get('eid') == '345' for m in res.json())


def test_list_rankings_when_there_are_rankings(client, session):
    # Given some records matching records in the database
    rank = RankingMatrix(
        eid='123',
        kind='',
        build_options='',
        ranking_matrix_path=''
    )
    session.add(rank)
    session.commit()
    # When I request the documents with the given bibliography eid
    _, res = client.get('/ranking')
    # Then I receive a successful response
    assert res.status == 200
    # The response is non empty
    assert len(res.json()) == 1
    # And has matrix
    assert any(m.get('eid') == '123' for m in res.json())


def test_individual_document_endpoint(client, session):
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
    _, res = client.get('/document/345')
    # Then I receive a successful response
    assert res.status == 200
    # And the response is non empty
    assert res.json().get('eid') == '345'


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


def test_single_bibliography_existing(client, session):
    # Given an existing bibliography
    bib = Bibliography(eid='123', description='lorem')
    session.add(bib)
    session.commit()
    # When I ask for it
    _, res = client.get('/bibliography/123')
    # Then I get a successful response
    assert res.status == 200
    # And the response is non empty
    assert res.json().get('eid') == '123'
    assert res.json().get('description') == 'lorem'


def test_bibliography_endpoint_eid_not_existing(client):
    # Given no bibliography in the database.
    _, res = client.get('/bibliography/346')
    # Then I receive a fail response
    assert res.status == 404
    # And the response is empty
    assert 'message' in res.json()


def test_document_endpoint_eid_not_existing(client):
    # Given no documents in the database.
    _, res = client.get('/document/346')
    # Then I receive a fail response
    assert res.status == 404
    # And the response is empty
    assert 'message' in res.json()


def test_bibliography_endpoint_when_many_bibliographies(client, session):
    # Create a bibliography
    bib = Bibliography(
        eid='345',
        description='lorem'
    )
    session.add(bib)
    session.commit()
    # When I request the list bibliography
    _, res = client.get('/bibliography')
    # Then I get a successful response
    assert res.status == 200
    # The response is non empty
    assert len(res.json()) == 1
    # And has bibliographies
    assert any(b.get('eid') == '345' for b in res.json())


def test_individual_matrix_endpoint_eid_not_existing(client):
    # Given no eid matrix in the database
    _, res = client.get('/matrix/346')
    # Then I receive a fail response
    assert res.status == 404
    # And the response is empty
    assert 'message' in res.json()
