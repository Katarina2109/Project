import mysql.connector
from mySQL_manager import *
from query_templates import *


def fetch_results(cursor, query, params=None):
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        print(f"Ошибка при получении результата: {e}")
        return []


def insert_keyword(connection, cursor, keyword):
    try:
        # Выполнение запроса на вставку
        cursor.execute(get_count_keywords_query, (keyword,))
        connection.commit()
        print(f"Ключевое слово '{keyword}' добавлено в таблицу.")

    except mysql.connector.Error as err:
        print(f"Ошибка при вставке ключевого слова: {err}")
