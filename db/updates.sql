--UPDATE book
--SET read_start = strftime('%Y-%m-%d', datetime(read_start, 'unixepoch'));

--UPDATE book
--SET
--    read_start='2022-11-21',
--    read_finish='2022-12-18'
--WHERE name='Чистый код :: Роберт Мартин';

--UPDATE book
--SET
--    read_start='2022-12-18',
--    read_finish='2022-12-31'
--WHERE name LIKE 'Теоретический минимум по Computer Science%';

--UPDATE book
--SET
--    read_start='2023-01-01',
--    read_finish='2023-02-12'
--WHERE name LIKE 'PostgreSQL. Основы языка SQL :: Евгений Моргунов';