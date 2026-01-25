import requests

# URL-адреса для логина и профиля
URL_LOGIN = "https://www.tarantool.io/ru/accounts/login/?next=/ru/plus/"
URL_PROFILE = "https://www.tarantool.io/ru/accounts/login/?next=/ru/plus/"

# Данные для авторизации
LOGIN_DATA = {
    "login": "test",
    "password": "test"
}

# Функция для парсинга атрибутов cookie
def parse_cookie_flags(set_cookie):
    flags = {
        "Secure": "Secure" in set_cookie,
        "HttpOnly": "HttpOnly" in set_cookie,
        "SameSite": "None"
    }
    if "SameSite=" in set_cookie:
        flags["SameSite"] = set_cookie.split("SameSite=")[1].split(";")[0]
    return flags

# Создаем сессию
s = requests.Session()

# Шаг 1: Отправляем запрос логина
print("[*] Отправляем запрос логина...")
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Referer": "https://site.test/login",
    "Origin": "https://site.test"
}

r = s.post(URL_LOGIN, data=LOGIN_DATA, headers=headers, allow_redirects=False)

print("Status:", r.status_code)

# Шаг 2: Печатаем заголовки ответа
print("\n[*] Заголовки ответа:")
for h, v in r.headers.items():
    if h.lower() == "set-cookie":
        print(v)

# Шаг 3: Печатаем cookies сессии
print("\n[*] Cookies в сессии:")
for c in s.cookies:
    print("Name:", c.name)
    print("Value:", c.value)
    print("Domain:", c.domain)
    print("Path:", c.path)
    print("Secure:", c.secure)
    print("HttpOnly:", "HttpOnly" in str(c))
    print("-" * 30)

# Шаг 4: Проверяем атрибуты cookie (Secure, HttpOnly, SameSite)
set_cookie = r.headers.get("Set-Cookie")
if set_cookie:
    flags = parse_cookie_flags(set_cookie)
    print("\n[*] Атрибуты cookie:")
    for k, v in flags.items():
        print(f"{k}: {v}")

# Шаг 5: Проверка фиксации сессии
print("\n[*] Cookie ДО логина:")
print(s.cookies.get_dict())

# Выполняем второй запрос, чтобы увидеть изменения cookie
r2 = s.post(URL_LOGIN, data=LOGIN_DATA)
print("\n[*] Cookie ПОСЛЕ логина:")
print(s.cookies.get_dict())

# Шаг 6: Проверка доступа без cookie
print("\n[*] Проверка доступа без cookie на профиль...")
s2 = requests.Session()
r2 = s2.get(URL_PROFILE)
print("Профиль без cookie:", r2.status_code)

# Шаг 7: Проверка доступа с cookie
print("\n[*] Проверка доступа с cookie на профиль...")
r3 = s.get(URL_PROFILE)
print("Профиль с cookie:", r3.status_code)

# Шаг 8: Проверка, меняется ли cookie после логина
if s.cookies.get_dict() != s2.cookies.get_dict():
    print("\n[*] Сессия изменяется после логина (не фиксируется).")
else:
    print("\n[*] Сессия фиксируется — сессионная фиксация.")