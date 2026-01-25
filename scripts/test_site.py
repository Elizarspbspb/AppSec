import requests
from bs4 import BeautifulSoup

# URL формы для входа на сайт
login_url = input("Введите URL формы входа: ")

# Пример SQL-инъекции, чтобы проверить форму на уязвимость
sql_injection_payload = "' OR '1'='1"
xss_payload = "<script>alert('XSS')</script>"

# Функция для тестирования SQL-инъекции
def test_sql_injection():
    payload = {
        "username": sql_injection_payload,
        "password": sql_injection_payload
    }
    response = requests.post(login_url, data=payload)
    if "ошибка" not in response.text.lower():  # Если не ошибка а успешный вход
        print("SQL инъекция возможна на форме входа!")
    else:
        print("SQL инъекция не сработала!")

# Функция для тестирования XSS
def test_xss():
    payload = {
        "username": xss_payload,
        "password": "password"
    }
    response = requests.post(login_url, data=payload)
    if xss_payload in response.text:
        print("XSS инъекция возможна на форме входа!")
    else:
        print("XSS инъекция не сработала!")

# Функция для тестирования авторизации через заголовки
def test_authorization():
    headers = {
        'Authorization': 'Bearer invalid_token'  # Пример неправильного токена
    }
    response = requests.get(login_url, headers=headers)
    if response.status_code == 401 or response.status_code == 403:
        print("Авторизация работает корректно, доступ не предоставлен.")
    else:
        print("Авторизация возможно не проверяется должным образом.")

# Функция для тестирования подмены сессионных куков (session hijacking)
def test_session_hijacking():
    # 1. Создаем сессию с действительными куками (например, с текущей сессией)
    session = requests.Session()

    # 2. Получаем страницу с личным кабинетом (предположим, что сессия уже активна)
    response = session.get(login_url)
    
    # Проверяем, если страница не требует авторизации
    if response.status_code == 200:
        print("Сессия активна. Пробуем подменить куки.")
        
        # 3. Подменяем сессионные куки на фальшивые
        session.cookies.set('session_id', 'fake_session_id')  # Фальшивый session_id

        # 4. Пробуем доступиться к странице с подмененным session_id
        response = session.get(login_url)

        if response.status_code == 200:
            print("Session Hijacking не работает, так как сервер проверяет куки.")
        else:
            print("Session Hijacking возможен! Смены сессии позволили получить доступ.")
    else:
        print("Не удалось получить доступ к личному кабинету с действительными куками.")

# Функция для тестирования логина
def test_login():
    # Тестируем SQL-инъекцию
    print("Тестируем на SQL-инъекцию...")
    test_sql_injection()
    
    # Тестируем на XSS
    print("Тестируем на XSS...")
    test_xss()

    # Тестируем на авторизацию
    print("Тестируем авторизацию...")
    test_authorization()

    # Тестируем на сессионный hijacking
    print("Тестируем на сессионный hijacking...")
    test_session_hijacking()

# Запуск тестов
test_login()