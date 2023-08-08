CREATE TABLE IF NOT EXISTS bot_user (
    telegram_id BIGINT PRIMARY KEY,
    created_at timestamp DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS book_category (
    id INTEGER PRIMARY KEY,
    created_at timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
    name VARCHAR(60) NOT NULL UNIQUE,
    ordering INTEGER NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS book (
    id INTEGER PRIMARY KEY,
    created_at timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
    name TEXT,
    ordering INTEGER NOT NULL,
    read_start DATE,
    read_finish DATE,
    category_id INTEGER,
    FOREIGN KEY(category_id) REFERENCES book_category(id),
    CHECK (read_start < read_finish)
    UNIQUE(category_id, ordering)
);
CREATE TABLE IF NOT EXISTS voting(
    id INTEGER PRIMARY KEY,
    voting_start DATE NOT NULL,
    voting_finish DATE NOT NULL,
    CHECK (voting_start < voting_finish)
);
CREATE TABLE IF NOT EXISTS vote(
    voting_id INTEGER,
    bot_user_telegram_id INTEGER,
    first_book_id INTEGER NOT NULL,
    second_book_id INTEGER NOT NULL,
    third_book_id INTEGER NOT NULL,
    FOREIGN KEY(voting_id) REFERENCES voting(id),
    FOREIGN KEY(bot_user_telegram_id) REFERENCES bot_user(telegram_id),
    FOREIGN KEY(first_book_id) REFERENCES book(id),
    FOREIGN KEY(second_book_id) REFERENCES book(id),
    FOREIGN KEY(third_book_id) REFERENCES book(id),
    PRIMARY KEY(voting_id, bot_user_telegram_id)
);
