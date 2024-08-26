import mysql.connector
from local_settings import dbconfig
from mySQL_manager import MySQLConnection
from query_templates import *



def execute_query(cursor, query, params=None):
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
    except Exception as e:
        print(f"Ошибка запроса: {e}")


def fetch_results(cursor, query, params=None):
    try:
        execute_query(cursor, query, params)
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


def show_popular_keywords(cursor):
    try:
        cursor.execute(get_popular_query)  # для получения популярных ключевых слов
        results = cursor.fetchall()  # получаем все результаты запроса

        if results:
            for row in results:
                print(f"Keyword: {row[0]}, Count: {row[1]}")
        else:
            print("Нет популярных запросов.")
    except Exception as e:
        print(f"Ошибка выполнения запроса: {e}")



if __name__ == '__main__':

    with MySQLConnection(dbconfig) as db:

        execute_query(db.cursor, get_table_keywords_query)
        db.connection.commit()  # сохранение изменений

        while True:
            print("\nВыберите действие:")
            print("1. Введите ключевое слово")
            print("2. Выберите жанр фильма из предоставленных")
            print("3. Введите год")
            print("4. Выберите жанр фильма и введите год")
            print("5. Список популярных запросов")
            print("0. Выход")

            choice = input("Введите номер действия: ")

            if choice == "1":
                keyword = input("Введите ключевое слово для поиска: ")
                insert_keyword(db.connection, db.cursor, keyword)

                # Вывод фильмов по ключевому слову
                films_query = f"%{keyword}%"
                results = fetch_results(db.cursor, get_films_by_keyword_query, (films_query,))
                if results:
                    print(f"Фильмы, содержащие ключевое слово '{keyword}':")
                    for row in results:
                        print(row)
                else:
                    print(f"Нет фильмов с ключевым словом '{keyword}'.")

            elif choice == "2":
                # Выбор жанра фильма из предоставленных
                print("Доступные жанры:")
                genres = fetch_results(db.cursor, get_category_query)
                genre_list = [genre[0] for genre in genres]
                for i, genre in enumerate(genre_list, 1):
                    print(f"{i}. {genre}")

                try:
                    genre_choice = int(input("Введите номер жанра для поиска: "))
                    if 1 <= genre_choice <= len(genre_list):
                        selected_genre = genre_list[genre_choice - 1]
                        results = fetch_results(db.cursor, get_film_genre_query, (selected_genre,))
                        if results:
                            print("Фильмы с выбранным жанром:")
                            for row in results:
                                print(row)
                        else:
                            print("Нет фильмов с таким жанром.")
                    else:
                        print("Неверный выбор номера жанра.")
                except ValueError:
                    print("Пожалуйста, введите корректный номер жанра.")

            elif choice == "3":
                # Поиск фильмов по году
                year = input("Введите год выпуска для поиска: ")
                results = fetch_results(db.cursor, get_film_year_query, (year,))
                if results:
                    print("Фильмы с выбранным годом:")
                    for row in results:
                        print(row)
                else:
                    print("Нет фильмов с таким годом.")

            elif choice == "4":
                # Поиск фильмов по жанру и году
                print("Доступные жанры:")
                genres = fetch_results(db.cursor, get_category_query)
                genre_list = [genre[0] for genre in genres]
                for i, genre in enumerate(genre_list, 1):
                    print(f"{i}. {genre}")

                try:
                    genre_choice = int(input("Введите номер жанра для поиска: "))
                    if 1 <= genre_choice <= len(genre_list):
                        selected_genre = genre_list[genre_choice - 1]

                        year = input("Введите год выпуска для поиска: ")

                        results = fetch_results(db.cursor, get_film_genre_year_query, (selected_genre, year))
                        if results:
                            print("Фильмы с выбранным жанром и годом:")
                            for row in results:
                                print(row)
                        else:
                            print("Нет фильмов с таким жанром и годом.")
                    else:
                        print("Неверный выбор номера жанра.")
                except ValueError:
                    print("Пожалуйста, введите корректный номер жанра.")

            elif choice == "5":
                # Вывод популярных запросов
                print("Популярные запросы:")
                show_popular_keywords(db.cursor)

            elif choice == "0":
                # Выход из программы
                print("Выход из программы.")
                break

            else:
                print("Неверный ввод. Пожалуйста, выберите номер действия из меню.")