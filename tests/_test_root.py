from .conftest import test_app

def test_read_root(test_app):
    response = test_app.get('/')
    assert response.status_code == 200
    assert response.json() == {'Hello': "API!"}
