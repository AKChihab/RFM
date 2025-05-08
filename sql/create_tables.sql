-- DDL to (re)create the customers and orders tables

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS customers (
    customer_id   TEXT    PRIMARY KEY,
    signup_date   DATE    NOT NULL
);

CREATE TABLE IF NOT EXISTS orders (
    order_id      TEXT    PRIMARY KEY,
    customer_id   TEXT    NOT NULL,
    order_date    DATE    NOT NULL,
    order_amount  REAL    NOT NULL,
    FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
        ON DELETE CASCADE
);