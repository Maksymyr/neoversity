-- Фінальний проєкт. Пункт 1. Створення схеми та імпорт даних.

CREATE SCHEMA `pandemic`;

USE `pandemic`;


-- Дані з infectious_cases.csv завантажено в таблицю infectious_cases
-- майстром Table Data Import Wizard. Скільки записів завантажено:
SELECT COUNT(*) AS imported_rows FROM `infectious_cases`;
