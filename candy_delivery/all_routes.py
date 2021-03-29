from flask import request, Response, jsonify, Blueprint

from candy_delivery.couriers_PATCH import check_courier_to_change, edit_courier
from candy_delivery.couriers_POST import check_couriers, add_couriers
from candy_delivery.couriers_get import get_courier_info
from candy_delivery.oders_POST import check_orders, add_orders
from candy_delivery.orders_assign_POST import check_courier_id_json, get_orders
from candy_delivery.orders_complete_assign import check_order_complete, complete_order

bp = Blueprint('all_routes', __name__)


@bp.route('/couriers', methods=['POST'])  # 1
@bp.route('/couriers/<int:courier_id>', methods=['GET', 'PATCH'])  # 6, 2
def couriers(courier_id=None):
    """Here, the 1, 2, and 6 handlers are implemented"""
    if request.method == 'POST':
        """Uploads the list of couriers to the system"""
        couriers_json = request.json
        bad_couriers = check_couriers(couriers_json)
        if len(bad_couriers["validation_error"]["couriers"]) != 0:
            return bad_couriers, 400
        return jsonify(add_couriers(couriers_json)), 201
    if request.method == 'GET':
        """Gets information about the courier"""
        courier_info = get_courier_info(courier_id)
        if courier_info == "Not found":
            return Response(status=404)
        else:
            return courier_info, 200
    if request.method == 'PATCH':
        """Changes the information about the courier"""
        data_to_change = request.json
        if check_courier_to_change(data_to_change):
            return edit_courier(courier_id, data_to_change), 201
        else:
            return Response(status=400)


@bp.route('/orders', methods=['POST'])  # 3
def orders():
    """Loads orders"""
    orders_json = request.json
    bad_orders = check_orders(orders_json)
    if len(bad_orders["validation_error"]["orders"]) != 0:  # (Couriers who did not pass validation are zero)
        return bad_orders, 400
    return jsonify(add_orders(orders_json)), 201


@bp.route('/orders/assign', methods=['POST'])  # 4
def orders_assign():
    """Gives the courier orders"""
    courier_id_json = request.json
    if check_courier_id_json(courier_id_json):
        courier_id = courier_id_json['courier_id']
        return get_orders(courier_id), 201
    else:
        return Response(status=400)


@bp.route('/orders/complete', methods=['POST'])  # 5
def orders_complete():
    """Marks the order as completed"""
    order_complete = request.json
    if check_order_complete(order_complete):
        return complete_order(order_complete), 201
    else:
        return Response(status=400)
