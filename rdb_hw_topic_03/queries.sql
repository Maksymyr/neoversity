-- ДЗ 3. Завантаження даних та основи SQL. DQL команди.

USE `hw_03`;

-- Завдання 1.1. Усі стовпчики таблиці products.
SELECT *
FROM products;


-- Завдання 1.2. Тільки стовпчики name і phone з таблиці shippers.
SELECT name, phone
FROM shippers;


-- Завдання 2. Середня, максимальна та мінімальна ціна товару.
SELECT
    AVG(price) AS avg_price,
    MAX(price) AS max_price,
    MIN(price) AS min_price
FROM products;


-- Завдання 3. Унікальні пари (category_id, price),
-- відсортовані за спаданням ціни, перші 10 рядків.
SELECT DISTINCT category_id, price
FROM products
ORDER BY price DESC
LIMIT 10;


-- Завдання 4. Кількість товарів із ціною від 20 до 100 включно.
SELECT COUNT(*) AS products_count
FROM products
WHERE price BETWEEN 20 AND 100;


-- Завдання 5. Кількість товарів і середня ціна в розрізі постачальників.
SELECT
    supplier_id,
    COUNT(*)   AS products_count,
    AVG(price) AS avg_price
FROM products
GROUP BY supplier_id
ORDER BY supplier_id;
