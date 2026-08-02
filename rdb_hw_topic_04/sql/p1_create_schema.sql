-- Завдання 1. Створення бази даних для керування бібліотекою книг (DDL).

CREATE SCHEMA IF NOT EXISTS `LibraryManagement`
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;

USE `LibraryManagement`;


-- Автори
CREATE TABLE `authors` (
    `author_id`   INT NOT NULL AUTO_INCREMENT,
    `author_name` VARCHAR(100) NOT NULL,
    PRIMARY KEY (`author_id`)
) ENGINE = InnoDB;


-- Жанри
CREATE TABLE `genres` (
    `genre_id`   INT NOT NULL AUTO_INCREMENT,
    `genre_name` VARCHAR(100) NOT NULL,
    PRIMARY KEY (`genre_id`)
) ENGINE = InnoDB;


-- Книги. Посилаються на автора та жанр.
CREATE TABLE `books` (
    `book_id`          INT NOT NULL AUTO_INCREMENT,
    `title`            VARCHAR(255) NOT NULL,
    `publication_year` YEAR,
    `author_id`        INT,
    `genre_id`         INT,
    PRIMARY KEY (`book_id`),
    KEY `idx_books_author_id` (`author_id`),
    KEY `idx_books_genre_id` (`genre_id`),
    CONSTRAINT `fk_books_author`
        FOREIGN KEY (`author_id`) REFERENCES `authors` (`author_id`),
    CONSTRAINT `fk_books_genre`
        FOREIGN KEY (`genre_id`) REFERENCES `genres` (`genre_id`)
) ENGINE = InnoDB;


-- Користувачі бібліотеки
CREATE TABLE `users` (
    `user_id`  INT NOT NULL AUTO_INCREMENT,
    `username` VARCHAR(100) NOT NULL,
    `email`    VARCHAR(255),
    PRIMARY KEY (`user_id`)
) ENGINE = InnoDB;


-- Видані книги. Зв'язує книгу з користувачем, який її взяв.
CREATE TABLE `borrowed_books` (
    `borrow_id`   INT NOT NULL AUTO_INCREMENT,
    `book_id`     INT,
    `user_id`     INT,
    `borrow_date` DATE,
    `return_date` DATE,
    PRIMARY KEY (`borrow_id`),
    KEY `idx_borrowed_books_book_id` (`book_id`),
    KEY `idx_borrowed_books_user_id` (`user_id`),
    CONSTRAINT `fk_borrowed_books_book`
        FOREIGN KEY (`book_id`) REFERENCES `books` (`book_id`),
    CONSTRAINT `fk_borrowed_books_user`
        FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE = InnoDB;
