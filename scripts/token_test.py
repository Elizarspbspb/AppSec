import requests

# URL для логина
URL_LOGIN = "https://www.tarantool.io/ru/accounts/login/"

# Данные для логина
LOGIN_DATA = {
    "login": "your_username",  # Замените на ваш логин
    "password": "your_password",  # Замените на ваш пароль
    "csrfmiddlewaretoken": "W8l7C0Oh3pP0P3LuJF1F817lard5Ebx1LszyrDraLoR24xANUYTvd0ORj2hW7ieO"  # Используем CSRF токен
}

# Заголовки, полученные из DevTools
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded",
    "Cookie": "check-authenticated=; csrftoken=W8l7C0Oh3pP0P3LuJF1F817lard5Ebx1LszyrDraLoR24xANUYTvd0ORj2hW7ieO; sessionid=5bv15o0pjkn8ny3uzr10gm94i607f1ei; _ga_YHFL9RMBZ2=GS2.1.s1768831277$o1$g1$t1768833811$j50$l0$h0; _ga=GA1.2.1130180432.1768831277; _gid=GA1.2.261451613.1768831278; _ym_uid=1768831278404548059; _ym_d=1768831278; tmr_lvid=8b2e8b1e4a34d5ba4f064d39d12c9dae; tmr_lvidTS=1768831278460; _ym_isad=2; _ym_visorc=w; domain_sid=ZXxv2dR1JfcCMymxqJr0H%3A1768831278964; tmr_detect=0%7C1768833814307",
    "Host": "www.tarantool.io",
    "Origin": "https://www.tarantool.io",
    "Referer": "https://www.tarantool.io/ru/accounts/login/?next=/ru/plus/",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0"
}

# Сессия для повторного использования cookies
s = requests.Session()

# Отправляем запрос на логин
r = s.post(URL_LOGIN, data=LOGIN_DATA, headers=headers)

print("Статус:", r.status_code)
print("Ответ:", r.text)

# Печатаем cookies сессии после авторизации
print("\nCookies после логина:")
for cookie in s.cookies:
    print(f"{cookie.name}: {cookie.value}")