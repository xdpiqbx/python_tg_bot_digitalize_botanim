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
    UNIQUE(category_id, ordering),
    FOREIGN KEY(category_id) REFERENCES book_category(id)
);
CREATE TABLE IF NOT EXISTS voting(
    id INTEGER PRIMARY KEY,
    voting_start TIMESTAMP NOT NULL,
    voting_finish TIMESTAMP NOT NULL
);
CREATE TABLE IF NOT EXISTS vote(
    id INTEGER PRIMARY KEY,
    vote_id INTEGER,
    bot_user_telegram_id INTEGER,
    first_book INTEGER NOT NULL,
    second_book INTEGER NOT NULL,
    third_book INTEGER NOT NULL,
    FOREIGN KEY(vote_id) REFERENCES voting(id),
    FOREIGN KEY(bot_user_telegram_id) REFERENCES bot_user(telegram_id),
    FOREIGN KEY(first_book) REFERENCES book(id),
    FOREIGN KEY(second_book) REFERENCES book(id),
    FOREIGN KEY(third_book) REFERENCES book(id)
);
