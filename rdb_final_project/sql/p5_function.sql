-- Фінальний проєкт. Пункт 5. Власна функція різниці в роках.

USE `pandemic`;

DROP FUNCTION IF EXISTS `years_since_year`;

DELIMITER $$

CREATE FUNCTION `years_since_year`(p_year INT)
RETURNS INT
NOT DETERMINISTIC
NO SQL
BEGIN
    -- Функція приймає рік, будує з нього перше січня
    -- і повертає різницю в роках із поточною датою.
    IF p_year IS NULL THEN
        RETURN NULL;
    END IF;
    RETURN TIMESTAMPDIFF(YEAR, MAKEDATE(p_year, 1), CURDATE());
END$$

DELIMITER ;


-- Застосування функції до даних.
SELECT
    c.`id`,
    c.`year`,
    `years_since_year`(c.`year`) AS years_diff
FROM `cases` AS c
ORDER BY c.`id`;
