import pytest
from fastapi.testclient import TestClient

from .conftest import test_app
from app.constants import WRONG_SHAPE

# VALID_SHAPES = [
# #    size page begin end
#     [1,   0,   0,    0], # 0 # custom size
#     [1,   0,   0,    1], # 1 # interval [ end-(size+1) ; end )
#     [1,   0,   1,    0], # 2 # interval [ begin ; begin+size )
#     [1,   1,   0,    0], # 3 # custom size with pagination
#     [0,   0,   1,    1], # 4 # interval [ begin : end )
#     [0,   0,   0,    0], # 5 # default 20 elements
#     [0,   1,   0,    0], # 6 # default 20 elements per page and page number `page`
# ]

# testing query params validation

def test_query_shape_0(test_app: TestClient):
    query = {'size': 17}
    resp = test_app.get('/fake_users',
        params=query
    )
    assert resp.status_code == 200
    rj = resp.json()
    assert 'detail' in rj
    assert 'data' in rj
    assert 'status' in rj['detail']
    assert rj['detail']['status'] == 'success'
    assert rj['detail']['data-length'] == 17
    assert rj['detail']['msg'] == 'Got query params: size=17 seed=None page=None begin=None end=None'
    assert len(rj['data']) == 17

def test_query_shape_1(test_app: TestClient):
    query = {'size': 6, 'end': 20}
    resp = test_app.get('/fake_users',
        params=query
    )
    assert resp.status_code == 200
    rj = resp.json()
    assert rj['detail']['status'] == 'success'
    assert rj['detail']['data-length'] == 6
    assert rj['detail']['msg'] == 'Got query params: size=6 seed=None page=None begin=None end=20'
    assert len(rj['data']) == 6

def test_query_shape_2(test_app: TestClient):
    query = {'size': 12, 'begin': 8}
    resp = test_app.get('/fake_users',
        params=query
    )
    assert resp.status_code == 200
    rj = resp.json()
    assert rj['detail']['status'] == 'success'
    assert rj['detail']['data-length'] == 12
    assert rj['detail']['msg'] == 'Got query params: size=12 seed=None page=None begin=8 end=None'
    assert len(rj['data']) == 12

def test_query_shape_3(test_app: TestClient):
    query = {'size': 5, 'page': 3}
    resp = test_app.get('/fake_users',
        params=query
    )
    assert resp.status_code == 200
    rj = resp.json()
    assert rj['detail']['status'] == 'success'
    assert rj['detail']['data-length'] == 5
    assert rj['detail']['msg'] == 'Got query params: size=5 seed=None page=3 begin=None end=None'
    assert len(rj['data']) == 5

def test_query_shape_4(test_app: TestClient):
    query = {'begin': 9, 'end': 16}
    resp = test_app.get('/fake_users',
        params=query
    )
    assert resp.status_code == 200
    rj = resp.json()
    assert rj['detail']['status'] == 'success'
    assert rj['detail']['data-length'] == 7
    assert rj['detail']['msg'] == 'Got query params: size=None seed=None page=None begin=9 end=16'
    assert len(rj['data']) == 7

def test_query_shape_5(test_app: TestClient):
    query = {}
    resp = test_app.get('/fake_users',
        params=query
    )
    assert resp.status_code == 200
    rj = resp.json()
    assert rj['detail']['status'] == 'success'
    assert rj['detail']['data-length'] == 20
    assert rj['detail']['msg'] == 'Got query params: size=None seed=None page=None begin=None end=None'
    assert len(rj['data']) == 20

def test_query_shape_6(test_app: TestClient):
    query = {'page': 9}
    resp = test_app.get('/fake_users',
        params=query
    )
    assert resp.status_code == 200
    rj = resp.json()
    assert rj['detail']['status'] == 'success'
    assert rj['detail']['data-length'] == 20
    assert rj['detail']['msg'] == 'Got query params: size=None seed=None page=9 begin=None end=None'
    assert len(rj['data']) == 20

def test_query_bad_type(test_app: TestClient):
    query = {'size': 'potato'}
    resp = test_app.get('/fake_users',
        params=query
    )
    assert resp.status_code == 422
    rj = resp.json()
    assert rj['detail'][0]['msg'] == 'value is not a valid integer'

def test_query_wrong_shape(test_app: TestClient):
    query = {'size': 4, 'begin': 6, 'end': 20}
    resp = test_app.get('/fake_users',
        params=query
    )
    assert resp.status_code == 422
    rj = resp.json()
    assert rj['detail'][0]['msg'] == WRONG_SHAPE.format([1, 0, 1, 1])

def test_query_negative_param(test_app: TestClient):
    query = {'size': -137}
    resp = test_app.get('/fake_users',
        params=query
    )
    assert resp.status_code == 422
    rj = resp.json()
    assert rj['detail'][0]['msg'] == 'query params shouldn\'t be negative, -137 got'

