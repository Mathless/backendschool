from jsonschema import validate, ValidationError
from markupsafe import escape

from candy_delivery.db import get_db


def check_orders(orders_json):
    """Checks the received json. First the whole order, then each order individually."""
    orders_schema = {
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
        validate(instance=orders_json, schema=orders_schema)
    except ValidationError:
        return {"validation_error": {"orders": [escape('got something other than "data" array')]}}
    order_schema = {
        "type": "object",
        "properties": {
            "order_id": {
                "type": "integer"
            },
            "weight": {
                "type": "number"
            },
            "region": {
                "type": "integer",
                "minimum": 1,
            },
            "delivery_hours": {
                "type": "array",
                "items":
                    {
                        "type": "string"
                    },
                "minItems": 1,
                "uniqueItems": True
            }
        },
        "required": ["order_id", "weight", "region", "delivery_hours"],
        "additionalProperties": False
    }
    bad_orders = {"validation_error": {"orders": []}}
    for order in orders_json["data"]:
        try:
            validate(instance=order, schema=order_schema)
        except ValidationError:
            bad_orders["validation_error"]["orders"].append({"id": order["order_id"]})
    return bad_orders


def add_orders(orders_json):
    """Adds orders to the database"""
    db = get_db()
    orders_values = []
    good_orders = {"orders": []}
    for order in orders_json["data"]:
        for key in ["order_id", "weight", "region", "delivery_hours"]:
            if key == "delivery_hours":
                orders_values.append("#".join(order[key]))
            elif key == "region":
                orders_values.append(str(order[key]))
            else:
                orders_values.append(order[key])
        try:
            db.execute(
                "INSERT INTO orders (order_id, weight, region, delivery_hours) VALUES (?, ?, ?, ?)",
                orders_values
            )
            good_orders["orders"].append({"id": order["order_id"]})
        except ValidationError:
            pass
        orders_values = []
    db.commit()
    return good_orders
