-- Фінальний проєкт. Пункт 3. Статистика Number_rabies за сутностями.

USE `pandemic`;

-- Для кожної унікальної комбінації Entity + Code рахуємо середнє,
-- мінімальне, максимальне значення та суму Number_rabies.
--
-- Порожні значення відфільтровано. Під час нормалізації '' перетворено
-- на NULL, тому фільтр — IS NOT NULL. Агрегатні функції MySQL і так
-- ігнорують NULL, але явна умова прибирає з результату сутності, у яких
-- немає жодного виміру: без неї вони потрапили б у вибірку з AVG = NULL.

SELECT
    e.`id`                  AS entity_id,
    e.`entity`              AS entity,
    e.`code`                AS code,
    AVG(c.`number_rabies`)  AS avg_rabies,
    MIN(c.`number_rabies`)  AS min_rabies,
    MAX(c.`number_rabies`)  AS max_rabies,
    SUM(c.`number_rabies`)  AS sum_rabies
FROM `cases` AS c
JOIN `entities` AS e ON e.`id` = c.`entity_id`
WHERE c.`number_rabies` IS NOT NULL
GROUP BY e.`id`, e.`entity`, e.`code`
ORDER BY avg_rabies DESC
LIMIT 10;
