import requests
import time

# Список заголовков для проверки
headers_to_test = [
    'Authorization', 'Cookie', 'Set-Cookie', 'Host', 'X-Forwarded-For', 
    'Origin', 'Access-Control-Allow-Origin', 'Content-Type', 'Transfer-Encoding', 
    'Content-Length', 'Referer', 'User-Agent', 'Location', 'WWW-Authenticate', 
    'Cache-Control', 'X-Request-ID', 'X-Real-IP', 'X-User', 'X-Role', 
    'X-Admin', 'X-Internal', 'X-Auth-Token'
]

# Основной URL для теста
url = input("Введите URL сайта для теста (например, https://example.com): ")

# Функция для выполнения тестов
def test_headers(url):
    for header in headers_to_test:
        print(f"Тестирование заголовка: {header}")
        try:
            # Отправляем запрос с подменой заголовка
            response = requests.get(url, headers={header: "Test"})
            
            # Выводим код ответа для каждого заголовка
            print(f"Код ответа для {header}: {response.status_code}")
            
            # Логика анализа кода ответа
            if response.status_code == 200:
                print(f"{header} - возможно уязвим, т.к. сервер не проверяет заголовок должным образом.")
            elif response.status_code == 401 or response.status_code == 403:
                print(f"{header} - проверка безопасности работает корректно (неудачная аутентификация/доступ).")
            else:
                print(f"{header} - код {response.status_code}, возможно сервер правильно фильтрует заголовок.")
        except Exception as e:
            print(f"Ошибка при проверке {header}: {e}")

        # Задержка для предотвращения DDoS-эффекта
        time.sleep(1)  # Задержка в 1 секунду

# Запуск теста
test_headers(url)