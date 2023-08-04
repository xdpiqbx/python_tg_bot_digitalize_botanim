import sqlite3
from db import query


class Database:
    def __init__(self):
        self.connection = sqlite3.connect('db/base.db')
        self.cursor = self.connection.cursor()

    def init_database(self):
        with open('init_database.sql', 'r') as sql_file:
            sql_text = sql_file.read()

        sql_queries = sql_text.split(';')
        print(sql_queries)

    # def create_table(self):
    #     self.cursor.execute(query.create_table_users())
    #     self.connection.commit()
    #
    # def add_new_user(self, user_data):
    #     self.cursor.execute(query.add_new_user(), user_data)
    #     self.connection.commit()
    #
    # def get_all_users(self):
    #     self.cursor.execute(query.select_all_users())
    #     return self.cursor.fetchall()
    #
    # def close(self):
    #     self.cursor.close()
    #     self.connection.close()
