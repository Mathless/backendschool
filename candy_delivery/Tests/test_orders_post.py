import json


def test_orders_post_201(client, app):
    with app.app_context():
        data = {
            "data": [
                {
                    "order_id": 20,
                    "weight": 0.23,
                    "region": 31,
                    "delivery_hours": ["09:00-18:00"]
                },
                {
                    "order_id": 21,
                    "weight": 15,
                    "region": 231,
                    "delivery_hours": ["09:00-18:00"]
                },
                {
                    "order_id": 22,
                    "weight": 0.01,
                    "region": 213,
                    "delivery_hours": ["09:00-12:00", "16:00-21:30"]
                }
            ]
        }
        url = '/orders'
        response = client.post(url, data=json.dumps(data), content_type='application/json', )

        assert response.status_code == 201
        assert json.dumps(response.get_json()) == json.dumps({
            "orders": [
                {
                    "id": 20
                },
                {
                    "id": 21
                },
                {
                    "id": 22
                }
            ]
        })


def test_orders_post_400(client, app):
    with app.app_context():
        data = {
            "data": [
                {
                    "order_id": 20,
                    "weight": 0.23,
                    "region": "",
                    "delivery_hours": ["09:00-18:00"]
                },
                {
                    "order_id": 21,
                    "region": 231,
                    "delivery_hours": ["09:00-18:00"]
                },
                {
                    "order_id": 22,
                    "weight": 0.01,
                    "region": 213,
                    "delivery_hours": ["09:00-12:00", "16:00-21:30"]
                }
            ]
        }
        url = '/orders'
        response = client.post(url, data=json.dumps(data), content_type='application/json', )

        assert response.status_code == 400
