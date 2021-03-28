import json


def test_couriers_get_201(client, app):
    with app.app_context():
        url = '/couriers/1'
        response = client.get(url)
        assert response.status_code == 200
        assert json.dumps(response.get_json()) == json.dumps({
            "courier_id": 1,
            "courier_type": "bike",
            "regions": [
                3,
                1,
                2
            ],
            "working_hours": [
                "11:35-14:05",
                "15:00-20:00"
            ]
        })


def test_couriers_get_400(client, app):
    with app.app_context():
        url = '/couriers/66666'
        response = client.get(url)
        assert response.status_code == 404
