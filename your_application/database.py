import pymysql  # Если вы используете pymysql
import mariadb  # Если вы используете mariadb

def get_connection():
    # Параметры подключения
    connection = pymysql.connect(
        host='localhost',  # или IP-адрес вашего сервера
        user='your_username',
        password='your_password',
        database='your_database'
    )
    return connection


def get_connection():
    # Параметры подключения
    connection = mariadb.connect(
        host='localhost',  # или IP-адрес вашего сервера
        user='your_username',
        password='your_password',
        database='your_database'
    )
    return connection