import sqlite3
import re
import os

DB_FILE = 'data/database.db'

def init_db():
    # Создание подключения к базе данных
    connection = sqlite3.connect(DB_FILE)

    cursor = connection.cursor()

    # Создаем таблицу users
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(30) NOT NULL UNIQUE,
    email VARCHAR(254) NOT NULL UNIQUE,
    password_hash TEXT NOT NULL CHECK(length(password_hash) >= 8) 
    )
    ''')

    # Сохраняем изменения
    connection.commit()

    # Закрываем соединение
    connection.close()

def get_user_by_username(username):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return user
'''
def get_password_by_password_hash(password_hash):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE password_hash = ?', (password_hash,))
    pass_hash = cursor.fetchone()
    conn.close()
    return pass_hash
''' 

def get_password_by_password_hash(username):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT password_hash FROM users WHERE username = ?', (username,))
    pass_hash = cursor.fetchone()
    conn.close()
    #return pass_hash
    if pass_hash is None:
        return None  # Пользователь не найден

    return pass_hash[0]  # Возвращаем первый элемент кортежа (строку хеша)
    
    
def create_user(username, email, password_hash):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',(username, email, password_hash))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False  # Пользователь с таким именем уже существует


init_db()