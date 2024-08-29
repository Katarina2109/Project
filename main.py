from prettytable import PrettyTable
from total_func import *
from query_templates import *

if __name__ == '__main__':

    with MySQLConnection(dbconfig) as db:

        db.execute_query(get_table_keywords_query)
        db.connection.commit()  # сохранение изменений

        while True:
            print("\nВыберите действие:")
            print("1. Поиск фильма по ключевому слову")
            print("2. Поиск фильма по жанру")
            print("3. Поиск фильма по году")
            print("4. Поиск фильма по жанру и году")
            print("5. Список популярных запросов")
            print("0. Выход")

            choice = input("Введите номер действия: ")

            if choice == "1":
                # Поиск фильма по ключевому слову
                keyword = input("Введите ключевое слово для поиска: ")
                insert_keyword(db.connection, db.cursor, keyword)

                page = 1  # 1-я страница
                results_per_page = 10  # Количество на 1 странице
                # Вывод фильмов по ключевому слову
                films_query = f"%{keyword}%"
                found_results = False

                while True:
                    offset = (page - 1) * results_per_page
                    paginated_query = get_films_by_keyword_query

                    results = fetch_results(db.cursor, get_films_by_keyword_query, (films_query, offset))

                    if results:
                        found_results = True
                        print(f"\nФильмы, содержащие ключевое слово '{keyword}' на странице {page}:")
                        table = PrettyTable(["Название фильма", "Жанр", "Год"])
                        for row in results:
                            title = row[0]
                            genre = row[1]
                            release_year = row[2]
                            table.add_row([title, genre, release_year])
                        print(table)

                        next_page = input("\nПоказать следующую страницу? (y/n): ").strip().lower()
                        if next_page == 'y':
                            page += 1
                        else:
                            break
                    else:
                        if not found_results:  # Если фильмы не были найдены ни на одной из страниц
                            print(f"\nНет фильмов с ключевым словом '{keyword}'.")
                        else:
                            print(f"\nЭто весь список по ключевому слову '{keyword}'.")
                        break

            elif choice == "2":
                # Поиск фильма по жанру
                print("Доступные жанры:")
                genres = fetch_results(db.cursor, get_category_query)
                genre_list = [genre[0] for genre in genres]
                for i, genre in enumerate(genre_list, 1):
                    print(f"{i}. {genre}")

                try:
                    genre_choice = int(input("Введите номер жанра для поиска: "))
                    if 1 <= genre_choice <= len(genre_list):
                        selected_genre = genre_list[genre_choice - 1]

                        page = 1
                        results_per_page = 10

                        while True:
                            offset = (page - 1) * results_per_page

                            results = fetch_results(db.cursor, get_film_genre_query, (selected_genre, offset))

                            if results:
                                print(f"\nФильмы с жанром '{selected_genre}' на странице {page}:")
                                table = PrettyTable(["Название фильма", "Жанр", "Год"])
                                for row in results:
                                    title = row[0]
                                    genre = row[1]
                                    release_year = row[2]
                                    table.add_row([title, genre, release_year])
                                print(table)

                                next_page = input("\nПоказать следующую страницу? (y/n): ").strip().lower()
                                if next_page == 'y':
                                    page += 1
                                else:
                                    break
                            else:
                                print(f"\nЭто весь список фильмов с жанром '{selected_genre}'.")
                                break
                    else:
                        print("\nНеверный выбор номера жанра.")
                except ValueError:
                    print("\nПожалуйста, введите корректный номер жанра.")

            elif choice == "3":
                # Поиск фильма по году
                year = input("Введите год выпуска для поиска: ")

                page = 1
                results_per_page = 10

                while True:
                    offset = (page - 1) * results_per_page

                    results = fetch_results(db.cursor, get_film_year_query, (year, offset))

                    if results:
                        print(f"\nФильмы с '{year}' годом на странице {page}:")
                        table = PrettyTable(["Название фильма", "Жанр", "Год"])
                        for row in results:
                            title = row[0]
                            genre = row[1]
                            release_year = row[2]
                            table.add_row([title, genre, release_year])
                        print(table)

                        next_page = input("\nПоказать следующую страницу? (y/n): ").strip().lower()
                        if next_page == 'y':
                            page += 1
                        else:
                            break

                    else:
                        if page == 1:
                            print(f"\nНет фильмов с '{year}' годом.")
                        else:
                            print(f"\nЭто весь список фильмов с '{year}' годом.")
                        break

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

                        page = 1
                        results_per_page = 10

                        while True:
                            offset = (page - 1) * results_per_page

                            results = fetch_results(db.cursor, get_film_genre_year_query,
                                                    (selected_genre, year, offset))
                            if results:
                                print(
                                    f"\nФильмы с выбранным жанром '{selected_genre}' и '{year}' годом на странице {page}:")
                                table = PrettyTable(["Название", "Жанр", "Год выпуска"])
                                for row in results:
                                    title = row[0]
                                    genre = row[1]
                                    release_year = row[2]
                                    table.add_row([title, genre, release_year])
                                print(table)

                                next_page = input("\nПоказать следующую страницу? (y/n): ").strip().lower()
                                if next_page == 'y':
                                    page += 1
                                else:
                                    break
                            else:
                                if page == 1:  # Если нет результатов на первой странице
                                    print(f"\nНет фильмов с жанром '{selected_genre}' и '{year}' годом.")
                                else:
                                    print(f"\nЭто весь список фильмов с жанром '{selected_genre}' и '{year}' годом.")
                                break

                    else:
                        print("\nНеверный выбор номера жанра.")

                except ValueError:
                    print("\nПожалуйста, введите корректный номер жанра.")

            elif choice == "5":
                # Вывод популярных запросов
                print("Популярные запросы:")

                page = 1
                results_per_page = 10

                while True:
                    offset = (page - 1) * results_per_page

                    results = fetch_results(db.cursor, get_popular_query, (results_per_page, offset))
                    if results:
                        table = PrettyTable(["Ключевое слово", "Количество"])
                        for row in results:
                            keyword = row[0]
                            count = row[1]
                            table.add_row([keyword, count])

                        print(f"\nРезультаты популярных запросов на странице {page}:")
                        print(table)

                        next_page = input("\nПоказать следующую страницу? (y/n): ").strip().lower()
                        if next_page == 'y':
                            page += 1
                        else:
                            break
                    else:
                        if page == 1:
                            print("\nНет популярных запросов.")
                        else:
                            print("\nЭто весь список популярных запросов.")
                        break

            elif choice == "0":
                # Выход из программы
                print("\nВыход из программы.")
                break

            else:
                print("\nНеверный ввод. Пожалуйста, выберите номер действия из меню.")
