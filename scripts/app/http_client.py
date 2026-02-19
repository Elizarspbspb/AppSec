import requests

def fetch(url):
    session = requests.Session()
    r = session.get(url, allow_redirects=True, timeout=10)

    return {
        "url": r.url,
        "status": r.status_code,
        "headers": r.headers,
        "cookies": r.cookies,
        "text": r.text
    }