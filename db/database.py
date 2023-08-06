import sqlite3


class Database:
    def __init__(self):
        self.connection = sqlite3.connect('base.db')
        self.cursor = self.connection.cursor()

    def execute_queries_from_sql_file(self, path_to_sql_file):
        with open(path_to_sql_file, 'r', encoding='utf-8') as sql_file:
            sql_text = sql_file.read()
        sql_queries = sql_text.split(';')

        for q in sql_queries:
            try:
                self.cursor.execute(q.strip())
            except sqlite3.OperationalError as error:
                print(q)
                print(error)
                self.connection.rollback()
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()


def main():
    db = Database()
    # db.execute_queries_from_sql_file('init_database.sql')
    # db.execute_queries_from_sql_file('init_insert_data.sql')
    db.close()


if __name__ == '__main__':
    main()
