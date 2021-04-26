import pytest


from backend.sc_database.model.Users import Users

from backend.app import create_app


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()
    testing_client = flask_app.test_client()
    ctx = flask_app.app_context()
    ctx.push()
    print('before')
    yield testing_client
    print('after')
    ctx.pop()

@pytest.fixture(scope='module')
def new_user():
    params = {
        "username": "Shemand",
        "full_name": "Nikolay Shemakov",
        "privileges": 1000,
        "Units_id": 2
    }
    user = Users(**params)
    return user
