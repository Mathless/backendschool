import datetime
from sqlite3 import Error

from jsonschema import validate, ValidationError

from candy_delivery.db import get_db


def check_courier_id_json(courier_id_json):
    """Checks the received json"""
    courier_id_schema = {
        "type": "object",
        "properties": {
            "courier_id": {
                "type": "integer"
            },
            "additionalProperties": False
        },
        "minProperties": 1,
        "additionalProperties": False
    }
    try:
        cursor = get_db().cursor()
        courier_id = courier_id_json["courier_id"]
        cursor.execute("SELECT count(*) FROM couriers WHERE courier_id = ?", (courier_id,))
        data = cursor.fetchone()[0]
        if data == 0:
            return False
        validate(instance=courier_id_json, schema=courier_id_schema)
    except (ValidationError, IndexError, Error):
        return False
    return True


def orders_json_to_string(json_orders):
    """Converts json orders to a string where the separator is '#'"""
    orders_s = ""
    for d in json_orders['orders']:
        orders_s += str(d['id']) + "#"
    return orders_s.strip("#")


# noinspection DuplicatedCode,DuplicatedCode
def check_dates_for_intersection(list_date_1, list_date_2):
    """Checks two dates for an intersection"""
    for date_1 in list_date_1:
        for date_2 in list_date_2:
            start1, end1 = date_1.split("-")
            start1 = start1.split(':')
            start1 = 60 * int(start1[0]) + int(start1[1])
            end1 = end1.split(':')
            end1 = 60 * int(end1[0]) + int(end1[1])
            start2, end2 = date_2.split("-")
            start2 = start2.split(':')
            start2 = 60 * int(start2[0]) + int(start2[1])
            end2 = end2.split(':')
            end2 = 60 * int(end2[0]) + int(end2[1])
            if start1 < end2 and start2 < end1:
                return True
    return False


def get_orders(courier_id):
    """Assigns the courier the maximum possible number of orders. To do this, go through the available orders in
order of increasing weight. If at least one order has been assigned, the assign_time issue time is recorded"""
    type_weight = {"foot": 10, "bike": 15, "car": 50}
    orders_for_response = {"orders": []}
    db = get_db()
    cursor = db.cursor()
    courier = list(cursor.execute("SELECT * FROM couriers WHERE courier_id = ?", [courier_id]))[0]
    working_hours = courier['working_hours'].strip("#").split("#")
    courier_regions = courier['regions'].strip("#").split("#")
    current_weight = courier['orders_weight']
    max_weight = type_weight[courier["courier_type"]]
    current_orders = courier['current_orders']
    for order in cursor.execute("SELECT * FROM orders WHERE status LIKE 'incomplete' ORDER BY weight"):
        if current_weight + order['weight'] < max_weight and order[
            'region'] in courier_regions and check_dates_for_intersection(working_hours,
                                                                          order['delivery_hours'].strip("#").split(
                                                                              "#")):
            current_weight += order['weight']
            db.execute(
                "UPDATE orders SET status='taken', courier_id=? WHERE order_id = ?", (courier_id, order['order_id'],)
            )
            orders_for_response["orders"].append({"id": order['order_id']})
        elif current_weight > max_weight:
            break

    if orders_for_response == {"orders": []}:
        for order_id in current_orders.strip("#").split("#"):
            if order_id == "":
                continue
            orders_for_response["orders"].append({"id": int(order_id)})
        if current_orders != "":
            orders_for_response["assign_time"] = courier["assign_time"]
        return orders_for_response
    assign_time = datetime.datetime.utcnow().isoformat("T") + "Z"
    orders_for_response["assign_time"] = assign_time
    for order_id in current_orders.strip("#").split("#"):
        if order_id == "":
            continue
        orders_for_response["orders"].append({"id": int(order_id)})
    current_orders = orders_json_to_string(orders_for_response)
    db.execute(
        "UPDATE couriers SET current_orders=?, orders_weight=?, assign_time=? WHERE courier_id = ?",
        (current_orders, current_weight, assign_time, courier['courier_id'])
    )
    if courier['last_time'] == "":
        db.execute(
            "UPDATE couriers SET last_time = ? WHERE courier_id = ?",
            (assign_time, courier['courier_id'])
        )
    db.commit()
    cursor.close()
    return orders_for_response
