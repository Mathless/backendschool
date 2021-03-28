DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

CREATE TABLE couriers
(
    courier_id       INTEGER UNIQUE NOT NULL,
    courier_type     TEXT           NOT NULL,
    regions          TEXT           NOT NULL,
    working_hours    TEXT           NOT NULL,
    current_orders   TEXT DEFAULT '',
    completed_orders TEXT DEFAULT '',
    orders_weight    REAL DEFAULT 0,
    assign_time      TEXT DEFAULT '',
    last_time        TEXT DEFAULT ''
);

CREATE TABLE orders
(
    order_id       INTEGER UNIQUE NOT NULL,
    weight         REAL           NOT NULL,
    region         TEXT           NOT NULL,
    delivery_hours TEXT           NOT NULL,
    status         TEXT           NOT NULL DEFAULT 'incomplete',
    courier_id     INTEGER                 DEFAULT -1,
    time           TEXT                    DEFAULT '',
    courier_type   TEXT
);