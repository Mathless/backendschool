INSERT INTO couriers (courier_id, courier_type, regions, working_hours, current_orders, completed_orders, orders_weight,
                      assign_time, last_time)
VALUES (1, 'bike', '3#1#2', '11:35-14:05#15:00-20:00', '6#4', '', 0.240000000000002, '2021-03-28T07:07:09.403198Z',
        '2021-03-28T07:07:09.403198Z');
INSERT INTO couriers (courier_id, courier_type, regions, working_hours, current_orders, completed_orders, orders_weight,
                      assign_time, last_time)
VALUES (2, 'car', '3#1#2', '11:35-14:05#15:00-20:00', '', '', 0, '', '');
INSERT INTO couriers (courier_id, courier_type, regions, working_hours, current_orders, completed_orders, orders_weight,
                      assign_time, last_time)
VALUES (3, 'foot', '31#231#213', '11:35-14:05#15:00-20:00', '', '', 0, '', '');
INSERT INTO couriers (courier_id, courier_type, regions, working_hours, current_orders, completed_orders, orders_weight,
                      assign_time, last_time)
VALUES (4, 'bike', '31#231#213', '11:35-14:05#15:00-20:00', '', '', 0, '', '');
INSERT INTO orders (order_id, weight, region, delivery_hours, status, courier_id, time, courier_type)
VALUES (1, 0.23, '12', '09:00-18:00', 'incomplete', -1, '', null);
INSERT INTO orders (order_id, weight, region, delivery_hours, status, courier_id, time, courier_type)
VALUES (2, 15, '1', '09:00-18:00', 'incomplete', -1, '', null);
INSERT INTO orders (order_id, weight, region, delivery_hours, status, courier_id, time, courier_type)
VALUES (3, 0.01, '22', '09:00-12:00#16:00-21:30', 'incomplete', -1, '', null);
INSERT INTO orders (order_id, weight, region, delivery_hours, status, courier_id, time, courier_type)
VALUES (4, 0.23, '1', '09:00-18:00', 'taken', 1, '', null);
INSERT INTO orders (order_id, weight, region, delivery_hours, status, courier_id, time, courier_type)
VALUES (5, 15, '2', '09:00-18:00', 'incomplete', -1, '', null);
INSERT INTO orders (order_id, weight, region, delivery_hours, status, courier_id, time, courier_type)
VALUES (6, 0.01, '3', '09:00-12:00#16:00-21:30', 'taken', 1, '', null);
INSERT INTO orders (order_id, weight, region, delivery_hours, status, courier_id, time, courier_type)
VALUES (7, 0.23, '4', '09:00-18:00', 'incomplete', -1, '', null);
INSERT INTO orders (order_id, weight, region, delivery_hours, status, courier_id, time, courier_type)
VALUES (8, 15, '5', '09:00-18:00', 'incomplete', -1, '', null);
INSERT INTO orders (order_id, weight, region, delivery_hours, status, courier_id, time, courier_type)
VALUES (9, 0.01, '6', '09:00-12:00#16:00-21:30', 'incomplete', -1, '', null);
INSERT INTO orders (order_id, weight, region, delivery_hours, status, courier_id, time, courier_type)
VALUES (10, 0.23, '4', '09:00-18:00', 'incomplete', -1, '', null);
INSERT INTO orders (order_id, weight, region, delivery_hours, status, courier_id, time, courier_type)
VALUES (11, 15, '5', '09:00-18:00', 'incomplete', -1, '', null);
INSERT INTO orders (order_id, weight, region, delivery_hours, status, courier_id, time, courier_type)
VALUES (12, 0.01, '6', '09:00-12:00#16:00-21:30', 'incomplete', -1, '', null);
INSERT INTO orders (order_id, weight, region, delivery_hours, status, courier_id, time, courier_type)
VALUES (13, 0.23, '31', '09:00-18:00', 'incomplete', -1, '', null);
INSERT INTO orders (order_id, weight, region, delivery_hours, status, courier_id, time, courier_type)
VALUES (14, 15, '231', '09:00-18:00', 'incomplete', -1, '', null);
INSERT INTO orders (order_id, weight, region, delivery_hours, status, courier_id, time, courier_type)
VALUES (15, 0.01, '213', '09:00-12:00#16:00-21:30', 'incomplete', -1, '', null);