-- Завдання 3. Об'єднання всіх восьми таблиць датасету з теми 3
-- за допомогою FROM та INNER JOIN.

USE `hw_03`;

-- Спільні ключі:
--   order_details.order_id   -> orders.id
--   order_details.product_id -> products.id
--   orders.customer_id       -> customers.id
--   orders.employee_id       -> employees.employee_id
--   orders.shipper_id        -> shippers.id
--   products.category_id     -> categories.id
--   products.supplier_id     -> suppliers.id

SELECT
    od.id          AS order_detail_id,
    o.id           AS order_id,
    o.`date`       AS order_date,
    c.name         AS customer_name,
    CONCAT(e.first_name, ' ', e.last_name) AS employee_name,
    sh.name        AS shipper_name,
    p.name         AS product_name,
    ct.name        AS category_name,
    su.name        AS supplier_name,
    od.quantity    AS quantity,
    p.price        AS price
FROM order_details AS od
INNER JOIN orders     AS o  ON od.order_id    = o.id
INNER JOIN customers  AS c  ON o.customer_id  = c.id
INNER JOIN employees  AS e  ON o.employee_id  = e.employee_id
INNER JOIN shippers   AS sh ON o.shipper_id   = sh.id
INNER JOIN products   AS p  ON od.product_id  = p.id
INNER JOIN categories AS ct ON p.category_id  = ct.id
INNER JOIN suppliers  AS su ON p.supplier_id  = su.id;
