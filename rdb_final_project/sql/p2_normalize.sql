-- Фінальний проєкт. Пункт 2. Нормалізація infectious_cases до 3НФ.

USE `pandemic`;


-- ------------------------------------------------------------------
-- Чому потрібна нормалізація.
--
-- У вихідній таблиці пара Entity + Code повторюється в кожному рядку:
-- 10521 запис на 245 унікальних сутностей. Code функціонально залежить
-- від Entity, а не від ключа рядка, тобто це транзитивна залежність —
-- порушення 3НФ.
--
-- Розділяємо на дві таблиці:
--   entities — довідник сутностей (Entity + Code), 245 рядків;
--   cases    — показники по роках із зовнішнім ключем на entities.
-- ------------------------------------------------------------------

DROP TABLE IF EXISTS `cases`;
DROP TABLE IF EXISTS `entities`;


-- Довідник сутностей: країна або регіон і його код.
CREATE TABLE `entities` (
    `id`     INT NOT NULL AUTO_INCREMENT,
    `entity` VARCHAR(100) NOT NULL,
    `code`   VARCHAR(10) NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uq_entities_entity` (`entity`)
) ENGINE = InnoDB;


-- Показники захворюваності по роках.
CREATE TABLE `cases` (
    `id`                   INT NOT NULL AUTO_INCREMENT,
    `entity_id`            INT NOT NULL,
    `year`                 INT NOT NULL,
    `number_yaws`          INT NULL,
    `polio_cases`          INT NULL,
    `cases_guinea_worm`    INT NULL,
    `number_rabies`        DOUBLE NULL,
    `number_malaria`       DOUBLE NULL,
    `number_hiv`           DOUBLE NULL,
    `number_tuberculosis`  DOUBLE NULL,
    `number_smallpox`      INT NULL,
    `number_cholera_cases` INT NULL,
    PRIMARY KEY (`id`),
    KEY `idx_cases_entity_id` (`entity_id`),
    CONSTRAINT `fk_cases_entity`
        FOREIGN KEY (`entity_id`) REFERENCES `entities` (`id`)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
) ENGINE = InnoDB;


-- Наповнення довідника: кожна сутність один раз.
INSERT INTO `entities` (`entity`, `code`)
SELECT DISTINCT `Entity`, NULLIF(`Code`, '')
FROM `infectious_cases`
ORDER BY `Entity`;


-- Наповнення таблиці показників.
-- NULLIF(...,'') перетворює порожні рядки на NULL, бо майстер імпорту
-- зберігає відсутні значення як '' незалежно від типу колонки.
INSERT INTO `cases` (
    `entity_id`, `year`, `number_yaws`, `polio_cases`, `cases_guinea_worm`,
    `number_rabies`, `number_malaria`, `number_hiv`, `number_tuberculosis`,
    `number_smallpox`, `number_cholera_cases`
)
SELECT
    e.`id`,
    CAST(NULLIF(ic.`Year`, '') AS UNSIGNED),
    CAST(NULLIF(ic.`Number_yaws`, '') AS SIGNED),
    CAST(NULLIF(ic.`polio_cases`, '') AS SIGNED),
    CAST(NULLIF(ic.`cases_guinea_worm`, '') AS SIGNED),
    NULLIF(ic.`Number_rabies`, '') + 0,
    NULLIF(ic.`Number_malaria`, '') + 0,
    NULLIF(ic.`Number_hiv`, '') + 0,
    NULLIF(ic.`Number_tuberculosis`, '') + 0,
    CAST(NULLIF(ic.`Number_smallpox`, '') AS SIGNED),
    CAST(NULLIF(ic.`Number_cholera_cases`, '') AS SIGNED)
FROM `infectious_cases` AS ic
JOIN `entities` AS e ON e.`entity` = ic.`Entity`;


-- Перевірка: жодного рядка не втрачено й не задубльовано.
SELECT
    (SELECT COUNT(*) FROM `infectious_cases`) AS rows_source,
    (SELECT COUNT(*) FROM `cases`)            AS rows_normalized,
    (SELECT COUNT(*) FROM `entities`)         AS entities_count;
