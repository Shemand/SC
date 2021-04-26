import base64
import json

from flask import jsonify

from backend.sc_actions.users import get_user, get_or_create_user
from backend.sc_common.authenticate import generate_token
from backend.sc_entities.Entities import Entities


def test_request_update_ad_computers(test_client):
    response = test_client.post('/api/v2/SZO/update/ad/computers')
    assert response.status_code == 200


def test_request_update_ad_users(test_client):
    response = test_client.post('/api/v2/SZO/update/ad/users')
    assert response.status_code == 200


def test_request_update_kaspersky(test_client):
    response = test_client.post('/api/v2/SZO/update/kaspersky')
    assert response.status_code == 200


def test_request_computers_not_loggined(test_client):
    response = test_client.get('/api/v2/SZO/computers')
    assert response.status_code == 401


def test_request_computers_loggined(test_client):
    database = Entities().get_district('SZO').database
    user = get_or_create_user(database, 'shemakovnd')
    token = generate_token(user.id)
    response = test_client.get('/api/v2/SZO/computers', headers={
        "Authorization" : f"jwt {token}"
    })
    data = json.loads(response.data)
    assert response.status_code == 200


def test_request_login(test_client):
    database = Entities().get_district('SZO').database
    user = get_or_create_user(database, 'shemakovnd')
    response = test_client.post('/api/v2/SZO/users/auth', json={
        "login": "shemakovnd",
        # "password": str(base64.b64encode('SHema98rg'.encode('utf-8')))
        "password": 'SHema98rg'
    })
    assert response.status_code == 200
    assert json.loads(response.data)['data']['jwt_token'] == generate_token(user.id)

# def test_request_update_structure(test_client):
#     response = test_client.post('/api/v2/SZO/update/reset/structure')
#     assert response.status_code == 200



