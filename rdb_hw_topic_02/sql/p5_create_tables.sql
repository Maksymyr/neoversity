-- ДЗ 2, пункт 5. Створення таблиць у базі даних за ER-діаграмою (3НФ).

CREATE SCHEMA IF NOT EXISTS `hw02_orders`
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;

USE `hw02_orders`;


-- Клієнти. Винесені в окрему таблицю на кроці 3НФ:
-- адреса залежить від клієнта, а не від замовлення.
CREATE TABLE `customers` (
    `customer_id`      INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `customer_name`    VARCHAR(100) NOT NULL,
    `customer_address` VARCHAR(255) NOT NULL,
    PRIMARY KEY (`customer_id`),
    UNIQUE KEY `uq_customers_name_address` (`customer_name`, `customer_address`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;


-- Товари. Довідник, щоб назва не повторювалася текстом у кожній позиції.
CREATE TABLE `products` (
    `product_id`   INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `product_name` VARCHAR(100) NOT NULL,
    PRIMARY KEY (`product_id`),
    UNIQUE KEY `uq_products_name` (`product_name`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;


-- Замовлення. Кожне належить рівно одному клієнту.
CREATE TABLE `orders` (
    `order_id`    INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `order_date`  DATE NOT NULL,
    `customer_id` INT UNSIGNED NOT NULL,
    PRIMARY KEY (`order_id`),
    KEY `idx_orders_customer_id` (`customer_id`),
    CONSTRAINT `fk_orders_customer`
        FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;


-- Позиції замовлення. Таблиця-зв'язка між замовленнями і товарами.
-- Складений ключ (order_id, product_id) не дає одному товару
-- потрапити в те саме замовлення двічі.
CREATE TABLE `order_items` (
    `order_id`   INT UNSIGNED NOT NULL,
    `product_id` INT UNSIGNED NOT NULL,
    `quantity`   INT UNSIGNED NOT NULL,
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
  COLLATE = utf8mb4_unicode_ci;
