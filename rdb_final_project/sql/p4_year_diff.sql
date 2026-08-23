-- Фінальний проєкт. Пункт 4. Різниця в роках вбудованими функціями.

USE `pandemic`;

-- Для колонки year будуємо три атрибути:
--   year_start_date — перше січня відповідного року (1996 -> 1996-01-01);
--   today           — поточна дата;
--   years_diff      — різниця між ними в роках.
--
-- MAKEDATE(year, 1) повертає дату за номером року й порядковим номером
-- дня в році, тобто перший день. TIMESTAMPDIFF рахує саме повні роки,
-- на відміну від DATEDIFF, який рахує дні.

SELECT
    c.`id`,
    c.`year`,
    MAKEDATE(c.`year`, 1)                                    AS year_start_date,
    CURDATE()                                                AS today,
    TIMESTAMPDIFF(YEAR, MAKEDATE(c.`year`, 1), CURDATE())    AS years_diff
FROM `cases` AS c
ORDER BY c.`id`;
