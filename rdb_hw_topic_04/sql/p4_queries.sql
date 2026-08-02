-- Завдання 4. Запити на основі об'єднання з завдання 3.

USE `hw_03`;


-- 4.1. Кількість рядків, які повертає запит із завдання 3.
SELECT COUNT(*) AS rows_count
FROM order_details AS od
INNER JOIN orders     AS o  ON od.order_id    = o.id
INNER JOIN customers  AS c  ON o.customer_id  = c.id
INNER JOIN employees  AS e  ON o.employee_id  = e.employee_id
INNER JOIN shippers   AS sh ON o.shipper_id   = sh.id
INNER JOIN products   AS p  ON od.product_id  = p.id
INNER JOIN categories AS ct ON p.category_id  = ct.id
INNER JOIN suppliers  AS su ON p.supplier_id  = su.id;


-- 4.2. Заміна декількох операторів INNER на LEFT та RIGHT.
-- Відповідь на питання «що відбувається з кількістю рядків і чому» —
-- у файлі README.md, розділ «Завдання 4.2».

-- Усі з'єднання замінено на LEFT.
SELECT COUNT(*) AS rows_count_all_left
FROM order_details AS od
LEFT JOIN orders     AS o  ON od.order_id    = o.id
LEFT JOIN customers  AS c  ON o.customer_id  = c.id
LEFT JOIN employees  AS e  ON o.employee_id  = e.employee_id
LEFT JOIN shippers   AS sh ON o.shipper_id   = sh.id
LEFT JOIN products   AS p  ON od.product_id  = p.id
LEFT JOIN categories AS ct ON p.category_id  = ct.id
LEFT JOIN suppliers  AS su ON p.supplier_id  = su.id;

-- З'єднання з customers замінено на RIGHT, решта залишились INNER.
SELECT COUNT(*) AS rows_count_right_customers
FROM order_details AS od
INNER JOIN orders     AS o  ON od.order_id    = o.id
RIGHT JOIN customers  AS c  ON o.customer_id  = c.id
INNER JOIN employees  AS e  ON o.employee_id  = e.employee_id
INNER JOIN shippers   AS sh ON o.shipper_id   = sh.id
INNER JOIN products   AS p  ON od.product_id  = p.id
INNER JOIN categories AS ct ON p.category_id  = ct.id
INNER JOIN suppliers  AS su ON p.supplier_id  = su.id;

-- Те саме RIGHT на customers, але всі з'єднання після нього — LEFT.
-- Порядок таблиць той самий, змінено лише оператори.
SELECT COUNT(*) AS rows_count_right_customers_then_left
FROM order_details AS od
INNER JOIN orders     AS o  ON od.order_id    = o.id
RIGHT JOIN customers  AS c  ON o.customer_id  = c.id
LEFT JOIN employees   AS e  ON o.employee_id  = e.employee_id
LEFT JOIN shippers    AS sh ON o.shipper_id   = sh.id
LEFT JOIN products    AS p  ON od.product_id  = p.id
LEFT JOIN categories  AS ct ON p.category_id  = ct.id
LEFT JOIN suppliers   AS su ON p.supplier_id  = su.id;


-- 4.3. Тільки рядки, де employee_id більший за 3 та не більший за 10.
SELECT COUNT(*) AS rows_count
FROM order_details AS od
INNER JOIN orders     AS o  ON od.order_id    = o.id
INNER JOIN customers  AS c  ON o.customer_id  = c.id
INNER JOIN employees  AS e  ON o.employee_id  = e.employee_id
INNER JOIN shippers   AS sh ON o.shipper_id   = sh.id
INNER JOIN products   AS p  ON od.product_id  = p.id
INNER JOIN categories AS ct ON p.category_id  = ct.id
INNER JOIN suppliers  AS su ON p.supplier_id  = su.id
WHERE o.employee_id > 3 AND o.employee_id <= 10;


-- 4.4. Групування за назвою категорії: кількість рядків і середня кількість товару.
SELECT
    ct.name        AS category_name,
    COUNT(*)       AS rows_count,
    AVG(od.quantity) AS avg_quantity
FROM order_details AS od
INNER JOIN orders     AS o  ON od.order_id    = o.id
INNER JOIN customers  AS c  ON o.customer_id  = c.id
INNER JOIN employees  AS e  ON o.employee_id  = e.employee_id
INNER JOIN shippers   AS sh ON o.shipper_id   = sh.id
INNER JOIN products   AS p  ON od.product_id  = p.id
INNER JOIN categories AS ct ON p.category_id  = ct.id
INNER JOIN suppliers  AS su ON p.supplier_id  = su.id
WHERE o.employee_id > 3 AND o.employee_id <= 10
GROUP BY ct.name;


-- 4.5. Фільтр груп: середня кількість товару більша за 21.
SELECT
    ct.name        AS category_name,
    COUNT(*)       AS rows_count,
    AVG(od.quantity) AS avg_quantity
FROM order_details AS od
INNER JOIN orders     AS o  ON od.order_id    = o.id
INNER JOIN customers  AS c  ON o.customer_id  = c.id
INNER JOIN employees  AS e  ON o.employee_id  = e.employee_id
INNER JOIN shippers   AS sh ON o.shipper_id   = sh.id
INNER JOIN products   AS p  ON od.product_id  = p.id
INNER JOIN categories AS ct ON p.category_id  = ct.id
INNER JOIN suppliers  AS su ON p.supplier_id  = su.id
WHERE o.employee_id > 3 AND o.employee_id <= 10
GROUP BY ct.name
HAVING AVG(od.quantity) > 21;


-- 4.6. Сортування за спаданням кількості рядків.
SELECT
    ct.name        AS category_name,
    COUNT(*)       AS rows_count,
    AVG(od.quantity) AS avg_quantity
FROM order_details AS od
INNER JOIN orders     AS o  ON od.order_id    = o.id
INNER JOIN customers  AS c  ON o.customer_id  = c.id
INNER JOIN employees  AS e  ON o.employee_id  = e.employee_id
INNER JOIN shippers   AS sh ON o.shipper_id   = sh.id
INNER JOIN products   AS p  ON od.product_id  = p.id
INNER JOIN categories AS ct ON p.category_id  = ct.id
INNER JOIN suppliers  AS su ON p.supplier_id  = su.id
WHERE o.employee_id > 3 AND o.employee_id <= 10
GROUP BY ct.name
HAVING AVG(od.quantity) > 21
ORDER BY rows_count DESC;


-- 4.7. Чотири рядки з пропущеним першим.
SELECT
    ct.name        AS category_name,
    COUNT(*)       AS rows_count,
    AVG(od.quantity) AS avg_quantity
FROM order_details AS od
INNER JOIN orders     AS o  ON od.order_id    = o.id
INNER JOIN customers  AS c  ON o.customer_id  = c.id
INNER JOIN employees  AS e  ON o.employee_id  = e.employee_id
INNER JOIN shippers   AS sh ON o.shipper_id   = sh.id
INNER JOIN products   AS p  ON od.product_id  = p.id
INNER JOIN categories AS ct ON p.category_id  = ct.id
INNER JOIN suppliers  AS su ON p.supplier_id  = su.id
WHERE o.employee_id > 3 AND o.employee_id <= 10
GROUP BY ct.name
HAVING AVG(od.quantity) > 21
ORDER BY rows_count DESC
LIMIT 4 OFFSET 1;
