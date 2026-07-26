-- =============================================================================
--  ДЗ 2. Проєктування баз даних з використанням семантичних моделей
--  Пункт 5. Створення таблиць у БД на основі ER-діаграми (схема у 3НФ)
--
--  СКБД:    MySQL 8.4 (MySQL Workbench)
--  Схема:   hw02_orders
--  Таблиці: customers, products, orders, order_items
--
--  Скрипт створює тільки структуру (таблиці, колонки, ключі, зв'язки),
--  без даних — як вимагає умова завдання.
-- =============================================================================

CREATE SCHEMA IF NOT EXISTS `hw02_orders`
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;

USE `hw02_orders`;

-- Видаляємо у зворотному до створення порядку (спочатку залежні таблиці).
DROP TABLE IF EXISTS `order_items`;
DROP TABLE IF EXISTS `orders`;
DROP TABLE IF EXISTS `products`;
DROP TABLE IF EXISTS `customers`;


-- -----------------------------------------------------------------------------
-- 1. customers — довідник клієнтів
--    Винесений на кроці 3НФ: усуває транзитивну залежність
--    order_id -> customer_name -> customer_address.
-- -----------------------------------------------------------------------------
CREATE TABLE `customers` (
    `customer_id`      INT UNSIGNED NOT NULL AUTO_INCREMENT
                       COMMENT 'Первинний ключ клієнта (сурогатний)',
    `customer_name`    VARCHAR(100) NOT NULL
                       COMMENT 'Прізвище / назва клієнта, напр. "Мельник"',
    `customer_address` VARCHAR(255) NOT NULL
                       COMMENT 'Адреса клієнта, напр. "Хрещатик 1"',
    PRIMARY KEY (`customer_id`),
    UNIQUE KEY `uq_customers_name_address` (`customer_name`, `customer_address`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci
  COMMENT = 'Клієнти. Адреса зберігається один раз на клієнта (3НФ)';


-- -----------------------------------------------------------------------------
-- 2. products — довідник товарів
--    Винесений, щоб назва товару зберігалася в одному місці, а не повторювалася
--    текстом у кожній позиції замовлення.
-- -----------------------------------------------------------------------------
CREATE TABLE `products` (
    `product_id`   INT UNSIGNED NOT NULL AUTO_INCREMENT
                   COMMENT 'Первинний ключ товару (сурогатний)',
    `product_name` VARCHAR(100) NOT NULL
                   COMMENT 'Назва товару, напр. "Лептоп"',
    PRIMARY KEY (`product_id`),
    UNIQUE KEY `uq_products_name` (`product_name`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci
  COMMENT = 'Товари. Назва унікальна — один товар = один рядок';


-- -----------------------------------------------------------------------------
-- 3. orders — замовлення
--    Зв'язок: customers (1) --- (0..N) orders
--    Кожне замовлення належить рівно одному клієнту (customer_id NOT NULL).
-- -----------------------------------------------------------------------------
CREATE TABLE `orders` (
    `order_id`    INT UNSIGNED NOT NULL AUTO_INCREMENT
                  COMMENT 'Номер замовлення — первинний ключ',
    `order_date`  DATE NOT NULL
                  COMMENT 'Дата замовлення, напр. 2023-03-15',
    `customer_id` INT UNSIGNED NOT NULL
                  COMMENT 'Зовнішній ключ на клієнта-замовника',
    PRIMARY KEY (`order_id`),
    KEY `idx_orders_customer_id` (`customer_id`),
    CONSTRAINT `fk_orders_customer`
        FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci
  COMMENT = 'Замовлення. Атрибути клієнта тут не дублюються (3НФ)';


-- -----------------------------------------------------------------------------
-- 4. order_items — позиції замовлення (таблиця-зв'язка)
--    Розв'язує зв'язок "багато-до-багатьох" між orders і products.
--    Складений первинний ключ (order_id, product_id) гарантує, що один товар
--    трапляється в одному замовленні не більше одного разу.
--    Зв'язки: orders (1) --- (1..N) order_items (N) --- (1) products
-- -----------------------------------------------------------------------------
CREATE TABLE `order_items` (
    `order_id`   INT UNSIGNED NOT NULL
                 COMMENT 'Зовнішній ключ на замовлення',
    `product_id` INT UNSIGNED NOT NULL
                 COMMENT 'Зовнішній ключ на товар',
    `quantity`   INT UNSIGNED NOT NULL
                 COMMENT 'Кількість одиниць товару в замовленні (> 0)',
    PRIMARY KEY (`order_id`, `product_id`),
    KEY `idx_order_items_product_id` (`product_id`),
    CONSTRAINT `fk_order_items_order`
        FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT `fk_order_items_product`
        FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    CONSTRAINT `chk_order_items_quantity` CHECK (`quantity` > 0)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci
  COMMENT = 'Позиції замовлення: який товар і в якій кількості замовлено';
