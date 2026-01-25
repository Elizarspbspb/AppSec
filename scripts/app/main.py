from http_client import fetch
from analyzers import headers, cookies, forms, js_surface, api_discovery

TARGET = "https://www.tarantool.io/ru/"

def main():
    resp = fetch(TARGET)

    findings = []
    findings += headers.analyze(resp["headers"])
    findings += cookies.analyze(resp["cookies"])
    findings += forms.analyze(resp["text"])
    findings += js_surface.analyze(resp["text"])
    findings += api_discovery.analyze(resp["text"])

    print(f"[+] Target: {resp['url']}")
    print(f"[+] Status: {resp['status']}\n")

    for f in findings:
        print(f)

if __name__ == "__main__":
    main()