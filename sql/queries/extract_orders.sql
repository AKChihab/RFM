-- Extract orders joined with customer signup date

SELECT
    o.order_id,
    o.customer_id,
    c.signup_date,
    o.order_date,
    o.order_amount
FROM orders AS o
JOIN customers AS c
  ON o.customer_id = c.customer_id
ORDER BY o.order_date DESC;