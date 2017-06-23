"""
Test the post methods.
"""
from condor.models import Bibliography


def test_matrix_creation_endpoint(client, session):
    bib = Bibliography(eid='123', description='lorem')
    session.add(bib)
    session.flush()
    response = client.post('/matrix', json={
        'bibliography': '123',
        'fields': ['title', 'description'],
    })
    assert response.status_code == 200
    assert response.json().get('bibliography_eid') == '123'


def test_matrix_creation_endpoint_fails(client, session):
    bib = Bibliography(eid='123', description='lorem')
    session.add(bib)
    session.flush()
    response = client.post('/matrix', json={
        'bibliography': '1234',
        'fields': ['title', 'description'],
    })
    assert response.status_code == 404
    assert 'message' in response.json()
