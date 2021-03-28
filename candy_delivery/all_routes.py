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
    """Здесь реализованы 1, 2 и 6 обработчики"""
    if request.method == 'POST':
        """Загружает список курьеров в систему"""
        couriers_json = request.json
        bad_couriers = check_couriers(couriers_json)
        if len(bad_couriers["validation_error"]["couriers"]) != 0:
            return bad_couriers, 400
        return jsonify(add_couriers(couriers_json)), 201
    if request.method == 'GET':
        """Получает информацию о курьере"""
        courier_info = get_courier_info(courier_id)
        if courier_info == "Not found":
            return Response(status=404)
        else:
            return courier_info, 200
    if request.method == 'PATCH':
        """Изменяет информацию о курьере"""
        data_to_change = request.json
        if check_courier_to_change(data_to_change):
            return edit_courier(courier_id, data_to_change), 201
        else:
            return Response(status=400)


@bp.route('/orders', methods=['POST'])  # 3
def orders():
    """Позволяет загрузить заказы"""
    orders_json = request.json
    bad_orders = check_orders(orders_json)
    if len(bad_orders["validation_error"]["orders"]) != 0:  # (курьеров с незаполненными полями ноль)
        return bad_orders, 400
    return jsonify(add_orders(orders_json)), 201


@bp.route('/orders/assign', methods=['POST'])  # 4
def orders_assign():
    """Позволяет получить курьеру заказы"""
    courier_id_json = request.json
    if check_courier_id_json(courier_id_json):
        courier_id = courier_id_json['courier_id']
        return get_orders(courier_id), 201
    else:
        return Response(status=400)


@bp.route('/orders/complete', methods=['POST'])  # 5
def orders_complete():
    """Позволяет отметить заказ выполненным"""
    order_complete = request.json
    if check_order_complete(order_complete):
        return complete_order(order_complete), 201
    else:
        return Response(status=400)
