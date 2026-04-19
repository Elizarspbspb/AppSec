import requests
from bs4 import BeautifulSoup
import time

URL = "https://best-proxies.ru/proxylist/free/"  # ← ВСТАВЬ СЮДА САЙТ

# 👉 ВСТАВЬ СЮДА СВОИ КУКИ (из браузера)
COOKIES = {
    # пример:
    # "sessionid": "abc123",
    # "cf_clearance": "xxx",
    "sid":"3zLBXpMwpTWhzkvIjCrlQrD3sP8F74Yt25-Z-Q8HXt3cFeqR-NfxZW3qIxgZvB4OP4%2CVKPbm0p6596dntY-cI0BPGBCYfXXpeo%2CoOso6Loh7R1-u98my2oAzsYP-Iy9f.7ce8930e4b31832ab0ac2df7bccbd4d182b77570ce9027273b82013572e24f16"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
}


def get_proxies():
    try:
        r = requests.get(URL, headers=HEADERS, cookies=COOKIES, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        proxies = []

        for a in soup.select("div.addr a"):
            ip_port = a.get_text(strip=True)

            # фильтр: только HTTPS (по родителю)
            parent = a.find_parent("div")
            if parent and "HTTPS" in parent.text:
                proxies.append(ip_port)

        return proxies

    except Exception as e:
        print("Ошибка:", e)
        return []


def save_to_file(proxies):
    with open("proxies.txt", "w") as f:
        for p in proxies:
            f.write(p + "\n")


while True:
    proxies = get_proxies()

    if proxies:
        print(f"[+] Найдено {len(proxies)} прокси")
        save_to_file(proxies)
    else:
        print("[-] Ничего не найдено")

    time.sleep(5)