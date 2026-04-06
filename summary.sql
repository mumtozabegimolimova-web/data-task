-- 1. Проверяем, что данные есть
SELECT COUNT(*) FROM books;

-- 2. Смотрим несколько строк (для видео)
SELECT * FROM books LIMIT 10;

-- 3. Удаляем summary таблицу, если уже была
DROP TABLE IF EXISTS books_summary;

-- 4. Создаём итоговую таблицу
CREATE TABLE books_summary AS
SELECT 
    publication_year,
    COUNT(*) AS book_count,
    ROUND(
        AVG(
            CASE 
                WHEN currency = '€' THEN price * 1.2
                ELSE price
            END
        ), 2
    ) AS average_price_usd
FROM books
GROUP BY publication_year
ORDER BY publication_year;

-- 5. Проверяем результат
SELECT * FROM books_summary;

-- 6. (по желанию — красиво отсортировано)
SELECT 
    publication_year,
    book_count,
    average_price_usd
FROM books_summary
ORDER BY publication_year;