-- Завдання 2. Наповнення таблиць тестовими даними (DML).

USE `LibraryManagement`;

INSERT INTO `authors` (`author_name`) VALUES
    ('Ліна Костенко'),
    ('Іван Багряний');

INSERT INTO `genres` (`genre_name`) VALUES
    ('Поезія'),
    ('Пригодницький роман');

INSERT INTO `books` (`title`, `publication_year`, `author_id`, `genre_id`) VALUES
    ('Маруся Чурай', 1979, 1, 1),
    ('Тигролови',    1944, 2, 2);

INSERT INTO `users` (`username`, `email`) VALUES
    ('oksana_p', 'oksana.p@example.com'),
    ('andrii_k', 'andrii.k@example.com');

-- Перша книга вже повернена, друга — ще на руках (return_date порожній).
INSERT INTO `borrowed_books` (`book_id`, `user_id`, `borrow_date`, `return_date`) VALUES
    (1, 1, '2024-03-04', '2024-03-18'),
    (2, 2, '2024-04-11', NULL);


-- Перевірка: вміст усіх п'яти таблиць в одному результаті.
SELECT
    b.book_id,
    b.title,
    b.publication_year,
    a.author_name,
    g.genre_name,
    u.username,
    u.email,
    bb.borrow_date,
    bb.return_date
FROM `books` AS b
INNER JOIN `authors` AS a ON b.author_id = a.author_id
INNER JOIN `genres`  AS g ON b.genre_id  = g.genre_id
LEFT  JOIN `borrowed_books` AS bb ON bb.book_id = b.book_id
LEFT  JOIN `users`   AS u  ON bb.user_id = u.user_id
ORDER BY b.book_id;
