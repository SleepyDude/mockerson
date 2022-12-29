from .conftest import test_app
import json
from fastapi.testclient import TestClient

def test_register(test_app: TestClient):
    data = {
        'username': 'JohnSmith',
        'password': 'jane_smith'
    }
    response = test_app.post('/register_user',
        content=json.dumps(data)
    )
    assert response.status_code == 200
    assert response.json() == {'Message':
        'Registration success. Welcome, JohnSmith!'}
