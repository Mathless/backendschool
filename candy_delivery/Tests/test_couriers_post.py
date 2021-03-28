import json

import pytest


@pytest.mark.parametrize("courier_type", ["foot", "bike", "car"])
@pytest.mark.parametrize("working_hours", ["11:35-14:05", "09:00-11:00"])
def test_couriers_201(client, app, courier_type, working_hours):
    with app.app_context():
        data = {
            "data": [
                {
                    "courier_id": 100,
                    "courier_type": courier_type,
                    "regions": [1, 12, 22],
                    "working_hours": ["11:35-14:05", "09:00-11:00"]
                }
            ]
        }
        url = '/couriers'
        print(data)
        response = client.post(url, data=json.dumps(data), content_type='application/json', )
        print(response.get_json(), "JSON")

        assert response.status_code == 201


@pytest.mark.parametrize("courier_type", ["pen", "cc", "wow"])
@pytest.mark.parametrize("working_hours", ["11:35-14:05", "09:00-11:00"])
def test_couriers_400(client, app, courier_type, working_hours):
    with app.app_context():
        data = {
            "data": [
                {
                    "courier_id": 100,
                    "courier_type": courier_type,
                    "regions": [1, 12],
                    "working_hours": ["11:35-14:05", "09:00-11:00"]
                }
            ]
        }
        url = '/couriers'
        print(data)
        response = client.post(url, data=json.dumps(data), content_type='application/json', )
        print(response.get_json(), "JSON")

        assert response.status_code == 400
