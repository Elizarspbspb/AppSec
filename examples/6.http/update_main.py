from urllib.parse import urlparse, unquote
from urllib.parse import parse_qs
import ipaddress
import tldextract
import json


url = input("Введите URL: ")

# 1. Сохраняем исходный URL без изменений
raw_url = url

# 2. Декодируем percent-encoding
decoded_url = unquote(raw_url)

print("\nСырой URL:")
print(raw_url)

print("\nPercent-decoded URL:")
print(decoded_url)

# 3. Разбираем URL
parse_error = None

try:
    parsed = urlparse(decoded_url)
except ValueError as e:
    parse_error = str(e)
    parsed = None

if parsed:
    host = parsed.hostname
    host_type = ""

    print("\nКомпоненты URL:")
    print("Протокол:", parsed.scheme)
    print("Host:", host)

    try:
        port = parsed.port
    except ValueError:
        port = None
        print("Порт: не удалось определить")
    else:
        print("Порт:", port)

    print("Путь:", parsed.path)
    print("Query:", parsed.query)
    print("Fragment:", parsed.fragment)
    print("Username:", parsed.username)
    print("Password:", parsed.password)


# 4. Определяем IP или доменное имя
    subdomain = ""
    domain = ""
    zone = ""
    ip_version = None

    try:
        ip = ipaddress.ip_address(host)

        host_type = "IP"
        ip_version = ip.version

        print("Тип host: IP")
        print("Версия IP:", ip.version)

    except ValueError:
        host_type = "domain"

        print("Тип host: доменное имя")

        extract = tldextract.TLDExtract(suffix_list_urls=())
        extracted = extract(host)

        subdomain = extracted.subdomain
        domain = extracted.domain
        zone = extracted.suffix

        print("Поддомен:", subdomain)
        print("Домен:", domain)
        print("Зона:", zone)


# 5. Unicode-представление host
    unicode_host = host
    try:
        unicode_host = host.encode("ascii").decode("idna")
    except (UnicodeEncodeError, UnicodeDecodeError, AttributeError):
        pass
    print("Unicode host:", unicode_host)

# 6. OAuth 2.0
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
    
# 7. Формируем JSON
    result = {
        "raw_url": raw_url,
        "decoded_url": decoded_url,

        "scheme": parsed.scheme,
        "host": host,
        "port": port,
        "path": parsed.path,
        "query": parsed.query,
        "fragment": parsed.fragment,
        "username": parsed.username,
        "password": parsed.password,

        "type": host_type,
        "ip_version": ip_version,

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