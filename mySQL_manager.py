import mysql.connector
from local_settings import dbconfig
from query_templates import *


class MixinMySQLQuery:
    def simple_select(self, query, value):

        try:
            self.cursor.execute(query, (f"%{value}%",))
            rows = self.cursor.fetchall()
            return rows

        except Exception as e:
            print(f"{e.__class__.__name__}: {e}")
            return []

    def is_exist_table(self, table_name) -> bool:
        try:
            query = """SELECT COUNT(*)
                       FROM information_schema.tables 
                       WHERE table_schema = %s 
                       AND table_name = %s;"""
            self.cursor.execute(query, (self.dbconfig['database'], table_name))
            result = self.cursor.fetchone()
            return result[0] > 0

        except Exception as e:
            print(f"{e.__class__.__name__}: {e}")
            return False


class MySQLConnection(MixinMySQLQuery):
    def __init__(self, dbconfig):
        self.dbconfig = dbconfig
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.connection = mysql.connector.connect(**self.dbconfig)
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()


if __name__ == '__main__':
    with MySQLConnection(dbconfig) as db:

        # 1. Проверка создания подключения
        db.cursor.execute('SELECT film_id, title, release_year FROM film LIMIT 1;')
        rows = db.cursor.fetchall()

        if rows:
            try:
                assert rows[0] == (1, 'ACADEMY DINOSAUR', 2013), "Error!"
                assert rows[0] != (2, 'ACADEMY DINOSAUR', 2013), "Error!"

            except AssertionError as e:
                print(e)
        else:
            print("No data returned from the query.")

        # 2. Проверка метода .simple_select()
        rows = db.simple_select(s_query, 'ACADEMY')
        if rows:
            assert rows[0] == ('ACADEMY DINOSAUR',), "Error!"
            assert rows[0] != ('ACADEMY DINOSAUR', 'SomeOtherTitle'), "Error!"
        else:
            print("No data returned from simple_select query.")

        is_exist = db.is_exist_table('film')
        assert is_exist == True, "Error!"

        is_exist = db.is_exist_table('non_existent_table')
        assert is_exist == False, "Error!"

# print("Тесты успешно прошли!")
