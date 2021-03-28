import json

import pytest


@pytest.mark.parametrize("courier_type", ["foot", "bike", "car"])
@pytest.mark.parametrize("regions", [[1, 2, 3], [123, 900]])
@pytest.mark.parametrize("working_hours", [["11:35-14:05", "09:00-11:00"], ["09:00-11:00"]])
def test_couriers_patch_201(client, app, courier_type, regions, working_hours):
    with app.app_context():
        data = {
            "courier_type": courier_type,
            "regions": regions,
            "working_hours":
                working_hours
        }
        url = '/couriers/1'
        response = client.patch(url, data=json.dumps(data), content_type='application/json', )
        assert response.status_code == 201
        assert json.dumps(response.get_json()) == json.dumps({
            "courier_id": 1,
            "courier_type": courier_type,
            "regions": regions,
            "working_hours": working_hours
        })


@pytest.mark.parametrize("courier_type", ["bad", "bike", "car"])
@pytest.mark.parametrize("regions", [["wrong"]])
@pytest.mark.parametrize("working_hours", [["11:35-14:05", "09:00-11:00"], []])
def test_couriers_patch_400(client, app, courier_type, regions, working_hours):
    with app.app_context():
        data = {
            "courier_type": courier_type,
            "regions": regions,
            "working_hours":
                working_hours
        }
        url = '/couriers/1'
        response = client.patch(url, data=json.dumps(data), content_type='application/json', )
        assert response.status_code == 400
