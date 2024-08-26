from mysql.connector import connect, Error
from local_settings import dbconfig

try:
    # Устанавливаем соединение с базой данных
    connection = connect(**dbconfig)
    if connection.is_connected():
        print("Connection to the database was successful!")
        # Получаем информацию о сервере
        db_info = connection.get_server_info()
        print(f"Connected to MySQL Server version: {db_info}")

        # Создаем курсор для выполнения SQL-запросов
        cursor = connection.cursor()
        cursor.execute("SELECT DATABASE();")
        # Получаем и выводим название текущей базы данных
        record = cursor.fetchone()
        print(f"You're connected to database: {record}")

except Error as e:
    print(f"Error: {e}")

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")