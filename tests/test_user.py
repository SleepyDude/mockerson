from .conftest import test_app
import json
from fastapi.testclient import TestClient
import pytest
from fastapi import HTTPException

@pytest.fixture
def john_auth_data():
    return {
        'username': 'JohnSmith',
        'password': 'jane_smith'
    }

@pytest.fixture
def john_auth_headers(test_app: TestClient, john_auth_data):
    data = f"username={john_auth_data['username']}&password={john_auth_data['password']}"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = test_app.post('/token',
        content=data,
        headers=headers
    )
    print(response.json())
    token = response.json()['access_token']
    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }
    return headers

def test_register(test_app: TestClient):
    # success register
    data = {
        'username': 'JohnSmith',
        'password': 'jane_smith'
    }
    response = test_app.post('/user',
        content=json.dumps(data)
    )
    assert response.status_code == 200
    assert response.json() == {'Message':
        'Registration success. Welcome, JohnSmith!'}
    # failed register
    data_2 = {
        'username': 'johnSmith',
        'password': 'another user'
    }

    response = test_app.post('/user',
        content=json.dumps(data_2)
    )
    assert response.status_code == 409
    assert response.json() == {'detail':
        'Registration Failed. The user johnSmith is already exists.'}

# def test_get_token(test_app: TestClient):
#     # positive response
#     registered_user = {
#         'username': 'JohnSmith',
#         'password': 'jane_smith'
#     }
#     response = test_app.post('/token',
#         content=json.dumps(registered_user)
#     )
#     assert response.status_code == 200
#     res_j = response.json()
#     assert 'access_token' in res_j
#     assert 'token_type' in res_j
#     assert res_j['token_type'] == 'bearer'

#     # negative response
#     not_registered_user = {
#         'username': 'hacker666',
#         'password': '4815162342'
#     }
#     response = test_app.post('/token',
#         content=json.dumps(not_registered_user)
#     )
#     assert response.status_code == 401
#     assert response.json() == {'detail': 'Invalid creditnails'}

def test_delete_user(test_app: TestClient, john_auth_headers):
    # good deletion
    response = test_app.delete('/user',
        headers=john_auth_headers
    )
    assert response.status_code == 204

