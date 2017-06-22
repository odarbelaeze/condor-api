"""
Test the post methods.
"""
from condor.models import Bibliography


def test_matrix_creation_endpoint(client, session):
    bib = Bibliography(eid='123', description='lorem')
    session.add(bib)
    session.flush()

    response = client.post('/matrix', {
        'bibliography': '123',
        'fields': 'title,description',
    })

    response = client.get(f"/matrix/{response.json().get('eid')}")

    assert response.status_code == 200
    assert response.json().get('bibliography_eid') == '123'
