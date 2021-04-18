import sqlite3
from random import randint

# global db   # Сделал переменную глобальной
# global sql  # Сделал переменную глобальной

db = sqlite3.connect('server.db')   # Создал базу данных с названием 'server.db'
sql = db.cursor()   # Курсор нужен для работы с базой данных, добавление та другое...

sql.execute('''CREATE TABLE IF NOT EXISTS users ( 
        login TEXT, 
        password TEXT,                  
        cash BIGINT)
''')    # Создал таблицу с названием 'user', Так же создал столбцы, и присвоил им типы данных ( их всего 3 )

db.commit()     # Подтвердил создание Бд

# user_cash = input('Cash: ')


def reg():

    user_login = input('Login: ')  # Ввод логина юзером
    user_password = input('Password: ')  # Ввод пароля юзером

    sql.execute(f"SELECT login FROM users WHERE login = '{user_login}'")
    # Мы выбираем столбец 'login' с таблицы 'users'
    # Так же говорим проверить есть ли уже такой логин у нас в таблцие (login = '{user_login}')
    if sql.fetchone() is None:  # fetchone возвращает одну строку данных
        sql.execute(f"INSERT INTO users VALUES (?, ?, ?)", (user_login, user_password, 0))
        # Знаки вопроса похожи на метод вывода в питоне, где через % указываются их значения
        # Через INSERT записываем в нашу базу значение, которые в скобках
        db.commit()     # Подтверждаем действие

        print('Аккаунт зарегестрирован')
    else:
        print('Такая запись уже есть')

    return output()


def add_cash():

    users_login = input('Log in: ')
    number = randint(1, 2)

    sql.execute(f'SELECT login FROM users WHERE login = "{users_login}"')
    if sql.fetchone() is None:
        print('Такого аккаунта нету')
        reg()
    else:
        if number == 1:
            sql.execute(f'UPDATE users SET cash = {100} WHERE login = "{users_login}"')
            # UPDATE вводим новые значние (обновляем) в нашу таблицу 'users'
            # SET Добавить в столбец 'cash' новое значение
            db.commit()
        else:
            print('Выпало 2')
    return output()


def output():
    accounts = []
    for value in sql.execute("SELECT * FROM users"):    # Выбираем все значение (*) в нашей таблице 'users'
        accounts.append(value)
        print(value)    # Выводим значение на экран
    return accounts


print(add_cash())
