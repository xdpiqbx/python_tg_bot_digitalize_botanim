--UPDATE book
--SET read_start = strftime('%Y-%m-%d', datetime(read_start, 'unixepoch'));

UPDATE book
SET
    read_start='2022-11-21',
    read_finish='2022-12-18'
WHERE name='Чистый код :: Роберт Мартин';

UPDATE book
SET
    read_start='2022-12-18',
    read_finish='2022-12-31'
WHERE name LIKE 'Теоретический минимум по Computer Science%';

UPDATE book
SET
    read_start='2023-01-01',
    read_finish='2023-02-12'
WHERE name LIKE 'PostgreSQL. Основы языка SQL :: Евгений Моргунов';

UPDATE book
SET
    read_start='2023-08-01',
    read_finish='2023-09-01'
WHERE name LIKE 'Рефакторинг. Улучшение существующего кода%';

INSERT
    INTO voting(voting_start, voting_finish)
    VALUES ('2023-08-01', '2023-09-01');

INSERT INTO vote (voting_id, bot_user_telegram_id, first_book_id, second_book_id, third_book_id)
    VALUES
        (1, 123, 102, 103, 100),
        (1, 133, 100, 103, 101),
        (1, 223, 102, 101, 100),
        (1, 626, 93, 92, 94);
