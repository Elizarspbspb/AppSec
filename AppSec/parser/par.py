import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs
import re
import time

#BASE_URL = "http://62.173.140.174:36100" 
BASE_URL = "http://62.173.140.174:36102"
LOGIN_URL = BASE_URL
USERNAME = "admin"
PASSWORD = "admin"

COMMON_PATHS = [
    "/search", "/admin", "/api", "/dashboard",
    "/profile", "/upload", "/debug"
]

visited = set()
found_urls = set()
results = []

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (compatible; MiniScanner/2.0)"
})


# ------------------------
# 🔐 Авторизация
# ------------------------
def login():
    data = {
        "username": USERNAME,
        "password": PASSWORD
    }

    r = session.post(LOGIN_URL, data=data)
    print("[*] Login status:", r.status_code)


# ------------------------
# 🔍 Парсинг JS
# ------------------------
def extract_endpoints_from_js(js_text):
    endpoints = set()

    # /api/... или /search и т.д.
    matches = re.findall(r'["\\\'](/[^"\\\']+)["\\\']', js_text)
    for m in matches:
        if len(m) < 100:  # фильтр мусора
            endpoints.add(m)

    return endpoints


def analyze_js(js_url):
    full_url = urljoin(BASE_URL, js_url)

    try:
        r = session.get(full_url, timeout=5)
        endpoints = extract_endpoints_from_js(r.text)

        for ep in endpoints:
            full_ep = urljoin(BASE_URL, ep)
            found_urls.add(full_ep)

    except:
        pass


# ------------------------
# 📄 Анализ страницы
# ------------------------
def analyze_page(url, html):
    soup = BeautifulSoup(html, "html.parser")

    page_data = {
        "url": url,
        "get_params": list(parse_qs(urlparse(url).query).keys()),
        "forms": [],
        "js_files": []
    }

    # --- формы ---
    for form in soup.find_all("form"):
        action = form.get("action")
        if not action:
            action = url
        else:
            action = urljoin(url, action)

        form_info = {
            "action": action,
            "method": form.get("method", "GET").upper(),
            "inputs": []
        }

        for inp in form.find_all(["input", "textarea", "select"]):
            form_info["inputs"].append({
                "name": inp.get("name"),
                "type": inp.get("type", "text")
            })

        page_data["forms"].append(form_info)

    # --- JS ---
    for script in soup.find_all("script", src=True):
        js_src = script["src"]
        page_data["js_files"].append(js_src)
        analyze_js(js_src)

    return page_data


# ------------------------
# 🕷️ Crawl
# ------------------------
def crawl(url, depth=2):
    if url in visited or depth == 0:
        return

    visited.add(url)
    print(f"[+] Crawling: {url}")

    try:
        r = session.get(url, timeout=5)
    except:
        return

    page_info = analyze_page(url, r.text)
    results.append(page_info)

    soup = BeautifulSoup(r.text, "html.parser")

    # --- ссылки ---
    for a in soup.find_all("a", href=True):
        link = urljoin(BASE_URL, a["href"])

        if urlparse(link).netloc == urlparse(BASE_URL).netloc:
            crawl(link, depth - 1)

    time.sleep(0.5)


# ------------------------
# 🔎 Проверка common paths
# ------------------------
def check_common_paths():
    print("\n[*] Checking common paths...")

    for path in COMMON_PATHS:
        url = urljoin(BASE_URL, path)

        try:
            r = session.get(url, timeout=5)
            if r.status_code == 200:
                print("[FOUND]", url)
                found_urls.add(url)
        except:
            pass


# ------------------------
# 📊 Вывод
# ------------------------
def print_results():
    for page in results:
        print("\n" + "="*60)
        print("URL:", page["url"])

        if page["get_params"]:
            print(" GET params:", page["get_params"])

        if page["forms"]:
            print(" Forms:")
            for f in page["forms"]:
                print(f"  -> {f['method']} {f['action']}")
                for inp in f["inputs"]:
                    print("     ", inp)
                    
        if page["js_files"]:
            print(" JS files:", page["js_files"])

    if found_urls:
        print("\n" + "="*60)
        print("Discovered endpoints (JS + common paths):")
        for u in found_urls:
            print(" ", u)


# ------------------------
# 🚀 MAIN
# ------------------------
if __name__ == "__main__":
    login()
    crawl(BASE_URL, depth=3)
    check_common_paths()
    print_results()