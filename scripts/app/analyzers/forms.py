from bs4 import BeautifulSoup
from models.finding import Finding

def analyze(html):
    soup = BeautifulSoup(html, "html.parser")
    findings = []

    for i, form in enumerate(soup.find_all("form")):
        method = form.get("method", "GET").upper()
        action = form.get("action", "")

        has_csrf = any(
            "csrf" in (inp.get("name","").lower())
            for inp in form.find_all("input")
        )

        if method == "POST" and not has_csrf:
            findings.append(Finding(
                "CSRF",
                "POST form without CSRF token",
                "High",
                f"Action={action}",
                location=f"form[{i}]"
            ))

    return findings