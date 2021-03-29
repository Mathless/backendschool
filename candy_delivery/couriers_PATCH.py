from jsonschema import validate, ValidationError

from candy_delivery.db import get_db
from candy_delivery.orders_assign_POST import check_dates_for_intersection


def check_courier_to_change(courier_to_change):
    """Checks the received json"""
    courier_schema = {
        "type": "object",
        "properties": {
            "courier_type": {
                "enum": ["foot", "bike", "car"]
            },
            "regions": {
                "type": "array",
                "items":
                    {
                        "type": "integer"
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
            },
            "additionalProperties": False
        },
        "minProperties": 1,
        "maxProperties": 3,
        "additionalProperties": False
    }
    try:
        validate(instance=courier_to_change, schema=courier_schema)
    except ValidationError:
        return False
    return True


def edit_courier(courier_id, data_to_change):
    """Changes the information about the courier. If the courier had current orders, it removes orders that it can
no longer fulfill"""
    db = get_db()
    couriers_values = []
    for key in data_to_change.keys():
        if key == "regions" or key == "working_hours":
            couriers_values.append("#".join([str(x) for x in data_to_change[key]]))
        else:
            couriers_values.append(data_to_change[key])
    for field in data_to_change.keys():
        if field == "courier_type":
            db.execute(
                "UPDATE couriers SET courier_type = ? WHERE courier_id = ?",
                (data_to_change["courier_type"], courier_id)
            )
        elif field == "regions":
            db.execute(
                "UPDATE couriers SET regions = ? WHERE courier_id = ?",
                ("#".join([str(x) for x in data_to_change["regions"]]), courier_id)
            )
        elif field == "working_hours":
            db.execute(
                "UPDATE couriers SET working_hours = ? WHERE courier_id = ?",
                ("#".join([str(x) for x in data_to_change["working_hours"]]), courier_id)
            )
    # Go through the orders and find out which ones can no longer be separated
    cursor = db.cursor()
    courier = list(cursor.execute("SELECT * FROM couriers WHERE courier_id = ?", (courier_id,)))[0]
    if courier["current_orders"] == "":
        db.commit()
        return {
            "courier_id": courier_id,
            "courier_type": courier['courier_type'],
            "regions": list(map(int, courier["regions"].strip("#").split('#'))),
            "working_hours": courier['working_hours'].strip("#").split('#')
        }
    type_weight = {"foot": 10, "bike": 15, "car": 50}
    working_hours = courier['working_hours'].strip("#").split("#")
    courier_regions = courier['regions'].strip("#").split("#")
    current_weight = courier['orders_weight']
    max_weight = type_weight[courier["courier_type"]]
    current_orders = courier['current_orders'].strip("#").split("#")
    # First, we delete the ones that do not fit the time or region
    for order in cursor.execute(
            "SELECT * FROM orders WHERE status LIKE 'taken' AND courier_id LIKE ?  ORDER BY weight DESC",
            (courier_id,)):
        if order[
            'region'] not in courier_regions or not check_dates_for_intersection(working_hours,
                                                                                 order['delivery_hours'].strip(
                                                                                     "#").split("#")):
            current_orders.remove(str(order["order_id"]))
            current_weight -= order['weight']
            db.execute(
                "UPDATE orders SET status='incomplete', courier_id=-1, time = '' WHERE order_id = ?",
                (order['order_id'],)
            )
    # Then we remove the ones that do not fit the weight
    for order in cursor.execute(
            "SELECT * FROM orders WHERE status LIKE 'taken' AND courier_id LIKE ?  ORDER BY weight DESC",
            (courier_id,)):
        if current_weight > max_weight:
            current_orders.remove(str(order["order_id"]))
            current_weight -= order['weight']
            db.execute(
                "UPDATE orders SET status='incomplete', courier_id=-1, time = '' WHERE order_id = ?",
                (order['order_id'],)
            )
        else:
            break
    current_orders = "#".join(current_orders)
    db.execute(
        "UPDATE couriers SET current_orders=?, orders_weight=? WHERE courier_id = ?",
        (current_orders, current_weight, courier_id)
    )
    db.commit()
    cursor.close()
    return {
        "courier_id": courier_id,
        "courier_type": courier['courier_type'],
        "regions": list(map(int, courier["regions"].strip("#").split('#'))),
        "working_hours": courier['working_hours'].strip("#").split('#')
    }
