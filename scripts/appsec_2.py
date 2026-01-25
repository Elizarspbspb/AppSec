import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin

URL = "https://www.tarantool.io/ru/accounts/login/"   # <-- поменяй
TIMEOUT = 10

session = requests.Session()
session.headers.update({
    "User-Agent": "SurfaceScanner/1.0"
})


def scan_headers(resp):
    print("\n[HTTP HEADERS]")
    security_headers = [
        "Content-Security-Policy",
        "X-Frame-Options",
        "X-Content-Type-Options",
        "Referrer-Policy",
        "Strict-Transport-Security",
        "Access-Control-Allow-Origin"
    ]

    for h in security_headers:
        if h in resp.headers:
            print(f"[+] {h}: {resp.headers[h]}")
        else:
            print(f"[-] {h}: MISSING")


def scan_cookies(resp):
    print("\n[COOKIES]")
    if not resp.cookies:
        print("No cookies set")
        return

    for c in resp.cookies:
        print(f"\nCookie: {c.name}")
        print(f"  Value: {c.value}")
        print(f"  Secure: {c.secure}")
        print(f"  HttpOnly: {'httponly' in str(c._rest).lower()}")
        print(f"  SameSite: {c._rest.get('samesite', 'NOT SET')}")


def scan_forms(html, base_url):
    print("\n[FORMS]")
    soup = BeautifulSoup(html, "html.parser")
    forms = soup.find_all("form")

    if not forms:
        print("No forms found")
        return

    for i, f in enumerate(forms, 1):
        action = f.get("action")
        method = f.get("method", "GET").upper()
        full_action = urljoin(base_url, action) if action else base_url

        inputs = f.find_all("input")
        names = [inp.get("name") for inp in inputs if inp.get("name")]

        csrf = any("csrf" in (inp.get("name", "")).lower() for inp in inputs)

        print(f"\nForm #{i}")
        print(f"  Action: {full_action}")
        print(f"  Method: {method}")
        print(f"  Fields: {names}")
        print(f"  CSRF token: {'YES' if csrf else 'NO'}")


def scan_js_surface(html):
    print("\n[JAVASCRIPT SURFACE]")
    lines = html.splitlines()

    sinks = [
        "innerHTML",
        "outerHTML",
        "document.write",
        "eval(",
        "setTimeout(",
        "setInterval(",
        "location.href",
        "location.assign"
    ]

    sources = [
        "location.search",
        "location.hash",
        "document.cookie",
        "localStorage",
        "sessionStorage",
        "postMessage"
    ]

    for i, line in enumerate(lines, 1):
        for sink in sinks:
            if sink in line:
                print(f"[SINK] line {i}: {sink}")
                print(f"    {line.strip()}")

        for src in sources:
            if src in line:
                print(f"[SOURCE] line {i}: {src}")
                print(f"    {line.strip()}")


def scan_api_discovery(html):
    print("\n[API DISCOVERY]")
    api_patterns = [
        r"/api/[a-zA-Z0-9/_\-]+",
        r"/v[0-9]+/[a-zA-Z0-9/_\-]+",
        r"/graphql",
    ]

    found = set()
    for pattern in api_patterns:
        matches = re.findall(pattern, html)
        for m in matches:
            found.add(m)

    if not found:
        print("No API endpoints found")
        return

    for api in found:
        print(f"[API] {api}")


def main():
    print(f"[+] Fetching {URL}")
    r = session.get(URL, timeout=TIMEOUT, allow_redirects=True)

    print(f"[+] Status: {r.status_code}")

    scan_headers(r)
    scan_cookies(r)
    scan_forms(r.text, URL)
    scan_js_surface(r.text)
    scan_api_discovery(r.text)


if __name__ == "__main__":
    main()