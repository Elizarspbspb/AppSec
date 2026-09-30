from urllib.parse import urlparse
from urllib.parse import parse_qs
import ipaddress
import tldextract
import json

url = input("Введите URL: ")

parsed = urlparse(url)
host = parsed.hostname

print("\nРазбор URL:")

# Основные части
print("Протокол:", parsed.scheme)
print("Host:", host)
print("Порт:", parsed.port)
print("Путь:", parsed.path)
print("Query:", parsed.query)
print("Fragment:", parsed.fragment)

# Логин и пароль
print("Username:", parsed.username)
print("Password:", parsed.password)


# Проверяем IP или домен
try:
    ip = ipaddress.ip_address(host)

    print("Тип host: IP")
    print("Версия IP:", ip.version)

    subdomain = ""
    domain = ""
    zone = ""

except ValueError:
    print("Тип host: доменное имя")

    # Разбираем домен без обращения к интернету
    extract = tldextract.TLDExtract(suffix_list_urls=())
    extracted = extract(host)

    subdomain = extracted.subdomain
    domain = extracted.domain
    zone = extracted.suffix


print("Поддомен:", subdomain)
print("Домен:", domain)
print("Зона:", zone)


# IDN
try:
    unicode_host = host.encode("ascii").decode("idna")
    print("Unicode host:", unicode_host)
except (UnicodeEncodeError, UnicodeDecodeError):
    print("Unicode host:", host)

# OAuth 2.0
query_params = parse_qs(parsed.query)
oauth_names = [
    "client_id",
    "redirect_uri",
    "response_type",
    "scope",
    "state",
    "code_challenge",
    "code_challenge_method"
]

oauth_params = {}
for name in oauth_names:
    if name in query_params:
        oauth_params[name] = query_params[name]

print("\nQuery-параметры:")
for name, values in query_params.items():
    print(name, "=", values)

print("\nOAuth 2.0:")
print("OAuth-параметры:")
for name, values in oauth_params.items():
    print(name, "=", values)
        
# JSON
result = {
    "url": url,
    "scheme": parsed.scheme,
    "host": host,
    "port": parsed.port,
    "path": parsed.path,
    "query": parsed.query,
    "fragment": parsed.fragment,
    "username": parsed.username,
    "password": parsed.password,
    "type": "IP" if "ip" in locals() else "domain",
    "subdomain": subdomain,
    "domain": domain,
    "zone": zone,
    "unicode_host": unicode_host,
    "query_params": query_params,
    "oauth": oauth_params
}

with open("url_report.json", "w", encoding="utf-8") as file:
    json.dump(result, file, ensure_ascii=False, indent=4)

print("\nJSON-отчёт сохранён в url_report.json")