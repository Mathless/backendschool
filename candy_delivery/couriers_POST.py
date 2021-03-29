from sqlite3 import Error

from jsonschema import validate, ValidationError
from markupsafe import escape

from candy_delivery.db import get_db


def check_couriers(couriers_json):
    """Checks the received json. First all of them, then each courier individually."""
    couriers_schema = {
        "properties": {
            "data": {
                "type": "array",
                "items": [
                    {
                        "type": "object"
                    }
                ]}},
        "additionalProperties": False
    }
    try:
        validate(instance=couriers_json, schema=couriers_schema)
    except ValidationError:
        return {"validation_error": {"couriers": [escape('got something other than "data" array')]}}
    courier_schema = {
        "type": "object",
        "properties": {
            "courier_id": {
                "type": "integer"
            },
            "courier_type": {
                "enum": ["foot", "bike", "car"]
            },
            "regions": {
                "type": "array",
                "items":
                    {
                        "type": "integer",
                        "minimum": 1
                    },
                "minItems": 1,
                "uniqueItems": True
            },
            "working_hours": {
                "type": "array",
                "items":
                    {
                        "type": "string"
                    },
                "minItems": 1,
                "uniqueItems": True
            }
        },
        "required": ["courier_id", "courier_type", "regions", "working_hours"],
        "additionalProperties": False
    }
    bad_couriers = {"validation_error": {"couriers": []}}
    for courier in couriers_json["data"]:
        try:
            validate(instance=courier, schema=courier_schema)
        except ValidationError:
            bad_couriers["validation_error"]["couriers"].append({"id": courier["courier_id"]})
    return bad_couriers


def add_couriers(couriers_json):
    """Adds couriers to the database"""
    db = get_db()
    couriers_values = []
    good_couriers = {"couriers": []}
    for courier in couriers_json["data"]:
        for key in ["courier_id", "courier_type", "regions", "working_hours"]:

            if key == "regions" or key == "working_hours":
                couriers_values.append("#".join([str(x) for x in courier[key]]))
            else:
                couriers_values.append(courier[key])
        try:
            db.execute(
                "INSERT INTO couriers (courier_id, courier_type, regions, working_hours) VALUES (?, ?, ?, ?)",
                couriers_values
            )
            good_couriers["couriers"].append({"id": courier["courier_id"]})
        except Error:
            pass
        couriers_values = []
    db.commit()
    return good_couriers
