import json

import pytest


@pytest.mark.parametrize("courier_id", [1])
@pytest.mark.parametrize("order_id", [4])
def test_couriers_assign_201(client, app, courier_id, order_id):
    with app.app_context():
        data = {
            "courier_id": courier_id,
            "order_id": order_id,
            "complete_time": "2021-03-27T17:59:23.416092Z"
        }
        url = '/orders/complete'
        response = client.post(url, data=json.dumps(data), content_type='application/json', )

        assert response.status_code == 201
        assert json.dumps(response.get_json()) == json.dumps({'order_id': order_id})


@pytest.mark.parametrize("courier_id", [1, 2, 3, 4])
@pytest.mark.parametrize("order_id", [1, 2, 3, 5])
def test_couriers_assign_400(client, app, courier_id, order_id):
    with app.app_context():
        data = {
            "courier_id": courier_id,
            "order_id": order_id,
            "complete_time": "2021-03-27T17:59:23.416092Z"
        }
        url = '/orders/complete'
        response = client.post(url, data=json.dumps(data), content_type='application/json', )

        assert response.status_code == 400
