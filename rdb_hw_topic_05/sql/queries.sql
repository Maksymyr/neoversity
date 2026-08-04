-- ДЗ 5. Вкладені запити. Повторне використання коду.

USE `hw_03`;


-- ------------------------------------------------------------------
-- 1. Таблиця order_details і поле customer_id з orders для кожного рядка.
--    Вкладений запит стоїть в операторі SELECT.
-- ------------------------------------------------------------------
SELECT
    od.*,
    (SELECT o.customer_id
     FROM orders AS o
     WHERE o.id = od.order_id) AS customer_id
FROM order_details AS od;


-- ------------------------------------------------------------------
-- 2. Таблиця order_details, відфільтрована так, щоб відповідне
--    замовлення мало shipper_id = 3.
--    Вкладений запит стоїть в операторі WHERE.
-- ------------------------------------------------------------------
SELECT od.*
FROM order_details AS od
WHERE od.order_id IN (SELECT o.id
                      FROM orders AS o
                      WHERE o.shipper_id = 3);


-- ------------------------------------------------------------------
-- 3. Середня кількість товару в розрізі замовлень, рахуючи лише
--    позиції з quantity > 10.
--    Вкладений запит стоїть в операторі FROM.
-- ------------------------------------------------------------------
SELECT
    t.order_id,
    AVG(t.quantity) AS avg_quantity
FROM (SELECT order_id, quantity
      FROM order_details
      WHERE quantity > 10) AS t
GROUP BY t.order_id;


-- ------------------------------------------------------------------
-- 4. Те саме завдання через оператор WITH.
-- ------------------------------------------------------------------
WITH temp AS (
    SELECT order_id, quantity
    FROM order_details
    WHERE quantity > 10
)
SELECT
    order_id,
    AVG(quantity) AS avg_quantity
FROM temp
GROUP BY order_id;


-- ------------------------------------------------------------------
-- 5. Функція ділення першого параметра на другий.
--    Обидва параметри та результат мають тип FLOAT.
-- ------------------------------------------------------------------
DROP FUNCTION IF EXISTS divide_floats;

DELIMITER $$

CREATE FUNCTION divide_floats(dividend FLOAT, divisor FLOAT)
RETURNS FLOAT
DETERMINISTIC
BEGIN
    -- Ділення на нуль повернуло б помилку, тому віддаємо NULL.
    IF divisor = 0 THEN
        RETURN NULL;
    END IF;
    RETURN dividend / divisor;
END$$

DELIMITER ;

-- Застосування функції до атрибута quantity. Другий параметр — 3.
SELECT
    id,
    order_id,
    product_id,
    quantity,
    divide_floats(quantity, 3) AS quantity_divided
FROM order_details;
