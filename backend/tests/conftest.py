import pytest



from backend.app import create_app
from backend.src.sc_repositories.DatabaseRepository import DatabaseRepository


# @pytest.fixture(scope='module')
# def test_client():
#     flask_app = create_app()
#     testing_client = flask_app.test_client()
#     ctx = flask_app.app_context()
#     ctx.push()
#     print('before')
#     yield testing_client
#     print('after')
#     ctx.pop()
#
# @pytest.fixture(scope='module')
# def new_user():
#     params = {
#         "username": "Shemand",
#         "full_name": "Nikolay Shemakov",
#         "privileges": 1000,
#         "Units_id": 2
#     }
#     user = Users(**params)
#     return user

@pytest.fixture(scope='module')
def test_database_repository():
    config = {
        "ip": "localhost",
        "port": 5432,
        "database": "sc",
        "driver": "postgresql+psycopg2",
        "username": "shemand",
        "password": "qwerty"
    }
    db = DatabaseRepository(config)
    return db