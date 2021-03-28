from collections import defaultdict
from sqlite3 import Error

from candy_delivery.db import get_db


def get_courier_info(courier_id):
    """Получает информацию о курьере. Если курьер выполнил хотя бы один заказ, то рассчитывает для него рейтинг и
    заработок """
    db = get_db()
    cursor = db.cursor()
    try:
        courier = list(cursor.execute("SELECT * FROM couriers WHERE courier_id = ?", (courier_id,)))[0]
    except IndexError or Error:
        return "Not found"
    json_response = {
        "courier_id": courier_id,
        "courier_type": courier['courier_type'],
        "regions": list(map(int, courier["regions"].strip("#").split('#'))),
        "working_hours": courier['working_hours'].strip("#").split('#')
    }
    if courier['completed_orders'] == "":
        return json_response
    regions = courier['regions'].split("#")
    times_region = defaultdict(lambda: 0, {})
    times_region_counter = defaultdict(lambda: 0, {})
    type_k = {"foot": 2, "bike": 5, "car": 9}
    earnings = 0
    for region in regions:
        for time, courier_type in cursor.execute(
                "SELECT time, courier_type FROM orders WHERE region LIKE ? AND courier_id LIKE ?"
                " AND status LIKE 'completed'",
                (region, courier_id,)):
            times_region[region] = times_region.get(region, 0) + int(float(time))
            times_region_counter[region] = times_region_counter.get(region, 0) + 1
            earnings += 500 * type_k[courier_type]
    t = float('inf')
    for region in regions:
        if times_region_counter[region] == 0:
            continue
        t = min(t, times_region[region] // times_region_counter[region])
    rating = (60 * 60 - min(t, 60 * 60)) / (60 * 60) * 5
    json_response["rating"] = round(rating, 2)
    json_response["earnings"] = earnings
    return json_response
