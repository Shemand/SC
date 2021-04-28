import json

from backend.sc_actions.users import get_or_create_user
from backend.sc_common.authenticate import generate_token
from backend.sc_entities.Entities import Entities


def test_request_login(test_client):
    database = Entities().get_district('SZO').database
    user = get_or_create_user(database, 'shemakovnd')
    response = test_client.post('/api/v1/SZO/users/auth', json={
        "login": "shemakovnd",
        # "password": str(base64.b64encode('SHema98rg'.encode('utf-8')))
        "password": 'SHema98rg'
    })
    assert response.status_code == 200
    assert json.loads(response.data)['data']['jwt_token'] == generate_token(user.id)
