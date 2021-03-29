from sqlite3 import Error

import dateutil.parser
from jsonschema import validate, ValidationError

from candy_delivery.db import get_db


def check_order_complete(order_complete):
    """Checks json and if the order is not found, was assigned to another courier or not assigned at all,
    returns the HTTP 400 Bad Request error."""
    order_complete_schema = {
        "type": "object",
        "properties": {
            "courier_id": {
                "type": "integer"
            },
            "order_id": {
                "type": "integer"
            },
            "complete_time": {
                "type": "string"
            }
        },
        "required": ["courier_id", "order_id", "complete_time"],
        "additionalProperties": False
    }
    cursor = get_db().cursor()
    courier_id = order_complete["courier_id"]
    order_id = order_complete["order_id"]
    try:
        order = list(cursor.execute("SELECT * FROM orders WHERE order_id = ?", (order_id,)))[0]
        if order['status'] == "incomplete" or order['courier_id'] != courier_id:
            cursor.close()
            return False
        validate(instance=order_complete, schema=order_complete_schema)
    except (ValidationError, IndexError, Error, KeyError, ValueError, TypeError):
        cursor.close()
        return False
    cursor.close()
    return True


def complete_order(order_complete):
    """Marks the order as completed."""
    courier_id = order_complete["courier_id"]
    order_id = order_complete["order_id"]
    time = order_complete["complete_time"]
    db = get_db()
    cursor = get_db().cursor()
    cursor.execute(
        "SELECT current_orders, completed_orders, orders_weight, last_time, courier_type"
        " FROM couriers WHERE courier_id = ?",
        (courier_id,))
    current_orders, completed_orders, orders_weight, last_time, courier_type = cursor.fetchone()
    db.execute(
        "UPDATE orders SET status = 'completed', time = ?, courier_type = ? WHERE order_id = ?",
        (delay(last_time, time), courier_type,
         order_id))

    cursor.execute("SELECT weight FROM orders WHERE order_id = ?",
                   (order_id,))
    weight = cursor.fetchone()[0]
    list_current_orders = current_orders.strip("#").split("#")
    try:
        list_current_orders.remove(str(order_id))
    except ValueError:
        pass
    else:
        current_orders = "#".join(list_current_orders)
        completed_orders += "#" + str(order_id)
        orders_weight -= weight
        db.execute(
            "UPDATE couriers SET current_orders = ?, completed_orders = ?, orders_weight = ? WHERE courier_id = ?",
            (current_orders, completed_orders, orders_weight, courier_id)
        )
    db.commit()
    return {"order_id": order_id}


def delay(last_time, time):
    """Calculates the time in seconds between two dates in ISO 8601 format"""
    t_time = dateutil.parser.parse(time)
    l_time = dateutil.parser.parse(last_time)
    return abs(t_time - l_time).total_seconds()
