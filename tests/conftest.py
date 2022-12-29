import pytest
from fastapi.testclient import TestClient
import os
# os.environ['FASTAPI_TESTING'] = 'True' # the table names will change on testing

from app.app import app


@pytest.fixture(scope='module')
def test_app() -> TestClient:
    client = TestClient(app)
    yield client
