"""
Test the post methods.
"""


def test_matrix_creation_endpoint(client):
    response = client.post('/matrix', {
        'bibliography': '12312312',
        'fields': 'title,description',
    })
    print(response.json())
    assert response.status_code == 200
