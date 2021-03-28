import json

import pytest


@pytest.mark.parametrize("courier_id", [1, 2, 3, 4])
def test_couriers_assign_201(client, app, courier_id):
    with app.app_context():
        data = {
            "courier_id": courier_id
        }
        url = '/orders/assign'
        print(data)
        response = client.post(url, data=json.dumps(data), content_type='application/json', )
        print(response.get_json(), "JSON")

        assert response.status_code == 201


@pytest.mark.parametrize("courier_id", [111, 222, 333, 444])
def test_couriers_assign_400(client, app, courier_id):
    with app.app_context():
        data = {
            "courier_id": courier_id
        }
        url = '/orders/assign'
        print(data)
        response = client.post(url, data=json.dumps(data), content_type='application/json', )
        print(response.get_json(), "JSON")

        assert response.status_code == 400
