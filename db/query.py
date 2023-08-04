def create_table_users():
    return """
        CREATE TABLE IF NOT EXISTS bot_user (
            id INTEGER auto_increment PRIMARY KEY,
            created_at timestamp DEFAULT CURRENT_TIMESTAMP,
            telegram_id INT NOT NULL
        );
    """


def create_table_book_category():
    return """
        INSERT
            INTO users ('name', 'password')
            VALUES (?, ?);
    """


def select_all_users():
    return """
        SELECT name FROM users;
    """
