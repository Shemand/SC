# def test_request_update_ad_computers(test_client):
#     response = test_client.post('/api/v1/SZO/update/ad/computers')
#     assert response.status_code == 200
#
#
# def test_request_update_ad_users(test_client):
#     response = test_client.post('/api/v1/SZO/update/ad/users')
#     assert response.status_code == 200


def test_request_update_kaspersky(test_client):
    response = test_client.post('/api/v1/SZO/update/kaspersky')
    assert response.status_code == 200


# def test_request_update_dallas(test_client):
#     response = test_client.post('/api/v1/szo/update/dallas')
#     assert response.status_code == 200


# def test_request_update_puppet(test_client):
#     response = test_client.post('/api/v1/szo/update/puppet')
#     assert response.status_code == 200
