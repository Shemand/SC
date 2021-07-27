import json

from backend.sc_actions.users import get_or_create_user
from backend.sc_common.authenticate import generate_token
from backend.sc_entities.Entities import Entities


def test_request_computers_loggined(test_client):
    database = Entities().get_district('SZO').database
    user = get_or_create_user(database, 'shemakovnd')
    token = generate_token(user.id)
    response = test_client.get('/api/v1/SZO/computers', headers={
        "Authorization" : f"Bearer {token}"
    })
    data = json.loads(response.data)
    assert response.status_code == 200

def test_request_computers_not_loggined(test_client):
    response = test_client.get('/api/v1/SZO/computers')
    assert response.status_code == 401