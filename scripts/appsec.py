import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from collections import defaultdict

TARGET = "https://www.tarantool.io/ru/accounts/login/"  # <-- поменяй
TIMEOUT = 10

session = requests.Session()
session.headers.update({
    "User-Agent": "AppSec-Surface-Scanner/2.0"
})

print(f"\n[+] Target: {TARGET}")

r = session.get(TARGET, timeout=TIMEOUT)
html = r.text
lines = html.splitlines()

# ===============================
# Helper: find line numbers
# ===============================
def find_lines(keyword):
    hits = []
    for i, line in enumerate(lines, 1):
        if keyword in line:
            hits.append(i)
    return hits

# ===============================
# REPORT STRUCTURE
# ===============================
signals = defaultdict(list)

# ===============================
# 1. FORMS & INPUTS
# ===============================
soup = BeautifulSoup(html, "html.parser")
forms = soup.find_all("form")

for idx, f in enumerate(forms, 1):
    action = f.get("action", "")
    method = f.get("method", "GET").upper()
    full_action = urljoin(TARGET, action)

    inputs = f.find_all("input")
    for inp in inputs:
        name = inp.get("name")
        if not name:
            continue

        signals["Injection surface"].append({
            "location": full_action,
            "parameter": name,
            "method": method,
            "classes": ["SQLi", "XSS", "SSTI", "NoSQLi"]
        })

# ===============================
# 2. CSRF SURFACE
# ===============================
if forms:
    for f in forms:
        if f.get("method", "").lower() == "post":
            csrf = f.find("input", {"name": re.compile("csrf", re.I)})
            if not csrf:
                signals["CSRF surface"].append({
                    "location": urljoin(TARGET, f.get("action", "")),
                    "classes": ["CSRF", "Business Logic"]
                })

# ===============================
# 3. IDOR SURFACE
# ===============================
links = soup.find_all("a", href=True)
for a in links:
    href = a["href"]
    if re.search(r"/\d+", href) or re.search(r"id=\d+", href):
        signals["IDOR surface"].append({
            "location": href,
            "classes": ["IDOR", "Access Control"]
        })

# ===============================
# 4. CLIENT-SIDE JS
# ===============================
js_keywords = ["innerHTML", "document.write", "location", "eval"]
for kw in js_keywords:
    hits = find_lines(kw)
    for ln in hits:
        signals["Client-side JS"].append({
            "line": ln,
            "keyword": kw,
            "classes": ["DOM XSS", "Prototype Pollution"]
        })

# ===============================
# REPORT
# ===============================
print("\n========== SURFACE SCAN REPORT ==========\n")

for category, items in signals.items():
    print(f"[+] {category}")
    for item in items:
        print("   -", item)
    print()

print("[+] Scan finished.")