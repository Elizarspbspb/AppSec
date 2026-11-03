import os
import secrets
from flask import Flask
from secure import Secure

app = Flask(__name__)

# =====================================================================
# 1. КРИПТОГРАФИЧЕСКАЯ УСИЛЕННАЯ ГЕНЕРАЦИЯ И ХРАНЕНИЕ КЛЮЧА
# Ключ берем из переменных окружения хоста. Если ключа там нет -
# secrets.token_hex(32) генерирует криптографически случайный 64-символьный хэш.
app.secret_key = os.environ.get("FLASK_SECRET_KEY", secrets.token_hex(32))

# =====================================================================
# 2. НАСТРОЙКА БЕЗОПАСНОСТИ COOKIE
app.config['SESSION_COOKIE_HTTPONLY'] = True        # Защита от XSS (JS не прочитает куки)
app.config['SESSION_COOKIE_SECURE'] = True          # Только по HTTPS (Защита от Wireshark)
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'    # Максимальная защита от CSRF
# меняем имя сессии по умолчанию, чтобы убрать следы FLASK
app.config['SESSION_COOKIE_NAME'] = '__Secure-SESSION'

# =====================================================================
# 3. ПОДКЛЮЧЕНИЕ ЗАГОЛОВКОВ БЕЗОПАСНОСТИ (Security Headers)
# Библиотека secure для автоматической вставки заголовков
secure_headers = Secure()

# Перехват ответов сервера перед отправкой и добавление заголовков безопасности
@app.after_request
def set_security_headers(response):
    # 4. Внедряем базовые заголовки (X-Frame-Options: DENY, X-Content-Type-Options: nosniff и др.)
    secure_headers.framework.flask(response)
    
    # 5. CORS (Защита и разрешение доступа)
    # Категорически запрещено ставить '*', только доверенный Origin!
    response.headers['Access-Control-Allow-Origin'] = 'https://my/site.ru'
    # Разрешаем отправлять куки и JWT-токены в кросс-доменных запросах
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    # Разрешаем только безопасные методы
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    
    # 6. REFERRER-POLICY (Защита утечки ссылок)
    # При переходе на чужой сайт отдаем только Origin (https://my-1/site.ru),
    # чтобы не слить приватные пути и данные в реферере.
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    
    # 7. HSTS (Strict-Transport-Security)
    # На 1 год (31536000 сек) к сайту можно обращаться ТОЛЬКО по HTTPS. Запрещает HTTP.
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'
    
    # 8. Content Security Policy (CSP)
    # Разрешаем скрипты, стили и т.д. только с нашего домена ('self'). 
    # Блокировка инлайн-скриптов, XSS физически не сможет выполниться.
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self'; "
        "img-src 'self' data:; "
        "object-src 'none'; "
        "frame-ancestors 'none';"
    )
    return response

@app.route('/')
def index():
    return "Платформа успешно защищена на уровне стандартов ИБ-гигантов."

if __name__ == '__main__':
    # Запускается строго через Nginx + Gunicorn, 
    # но локально запускаем в безопасном режиме
    app.run(ssl_context='adhoc') # Локальный HTTPS для тестов
