import string

try:
   password = str(input()).replace(' ', '')
except ValueError:
   print('Enter only string, please')

# «Валидатор пароля»
def validate_password(password):
    upper = False
    lower = False
    digit = False
    punct = False
    if type(password) != str:
        return False        # Error
    if len(password) < 8:
        return False           # Error
    for i in password:
        if i in string.ascii_uppercase:
            upper = True
        if i in string.ascii_lowercase:
            lower = True
        if i in string.digits:
            digit = True
        if i in string.punctuation:
            punct = True
    if upper == False or lower == False or digit == False or punct == False:
        return False            # Error
    return True                 # Ok

if (validate_password(password) == False):
    print("Error password")  
else:
    print("Ok")
    print(len(password))
    print(password)

# --------------------------------------------------

# список найденных URL
white_port = [80, 22, 443, 3389]
black_port = [21, 23, 135]

try:
   port = int(input())
except ValueError:
   print('Enter only integer, please')

# «Сканер портов (симуляция)»
def scan_ports(port):
    for p in white_port:
        if port == p:
            print("Port", port, "is OPEN.")
            return
    for p in black_port:
        if port == p:
            print("Port", port, "is OPEN and considered VULNERABLE!")
            return
    print("Port", port, "is closed.")

scan_ports(port)

# --------------------------------------------------

logs = [ 
    "192.168.1.1 - - [01/Jan/2024] 'GET /index.html HTTP/1.1' 200",
    "10.0.0.5 - - [01/Jan/2024] 'POST /login.php HTTP/1.1' 404",
    "10.5.5.1 - - [01/Jan/2024] 'POST /login.php HTTP/1.1' 404",
    "10.5.5.0 - - [01/Jan/2024] 'POST /login.php HTTP/1.1' 404",
    "10.5.5.2 - - [01/Jan/2024] 'POST /login.php HTTP/1.1' 404",
    "10.5.5.0 - - [01/Jan/2024] 'POST /login.php HTTP/1.1' 404",
    "10.5.5.1 - - [01/Jan/2024] 'POST /login.php HTTP/1.1' 404",
    "192.168.1.1 - - [01/Jan/2024] 'GET /admin/panel HTTP/1.1' 403",
    "192.168.1.1 - - [01/Jan/2024] 'GET /admin/panel HTTP/1.1' 403",
    "192.168.1.2 - - [01/Jan/2024] 'GET /admin/panel HTTP/1.1' 403",
    "10.0.0.5 - - [01/Jan/2024] 'GET /index.html HTTP/1.1' 200",
    "192.168.1.1 - - [01/Jan/2024] 'POST /login.php HTTP/1.1' 200"
]

def find_suspicious_activity():
    scanners = []
    suspicious = []
    for l in logs:
        parts = l.split("'")
        result = []
        for i, part in enumerate(parts):
            if i % 2 == 1: 
                result.append(part)     # добавляет один элемент в конец списка
            else:
                subparts = part.split(' ')
                subparts = filter(None, subparts)
                result.extend(subparts) # добавляет каждый элемент из другого списка по отдельности

        if result[len(result)-1] == '404':
            x = len(scanners)
            not_found = True
            if x == 0:
                scanners.append(result[0])
                not_found = False
            else:
                while x != 0:
                    if scanners[x-1] == result[0]:
                        not_found = False
                    x -= 1
            if not_found == True:
                scanners.append(result[0])

        if result[len(result)-1] == '403':
            x = len(suspicious)
            forbidden = True
            if x == 0:
                suspicious.append(result[0])
                forbidden = False
            else:
                while x != 0:
                    if suspicious[x-1] == result[0]:
                        forbidden = False
                    x -= 1
            if forbidden == True:
                suspicious.append(result[0])

    my_tuple = (scanners, suspicious)
    print(my_tuple)

find_suspicious_activity()

# --------------------------------------------------

import bcrypt

user = {
    "username": "",
    "password_hash": b"",
    "failed_login_attempts": 0,
    "is_locked": False
}

try:
    print("Create login: ")
    username = str(input()).replace(' ', '')
    print("Create password: ")
    password = str(input())
except ValueError:
    print('Enter only string, please')

def create_user(username, password):
    bytes_password = password.encode('utf-8')
    hashed = bcrypt.hashpw(bytes_password, bcrypt.gensalt())
    print(hashed)
    failed_login = 0
    user['username'] = username
    user['password_hash'] = hashed

def authenticate_user(user, input_password):
    if user['is_locked'] == True:
        print("Account locked")
        return 1

    bytes_input_password = input_password.encode('utf-8') # Convert the string to bytes
    if bcrypt.checkpw(bytes_input_password, user['password_hash']):
        print("Login successful")
        user['failed_login_attempts'] = 0
        return 0
    else:
        print("Password Does Not Match")
        user['failed_login_attempts'] += 1
        if user['failed_login_attempts'] == 3:
            user['is_locked'] = True
            print("Account locked")
        return 1

create_user(username, password)

test = 1
while test != 0:
    try:
        print("Enter password: ")
        input_password = str(input())
    except ValueError:
        print('Enter only string, please')
    test = authenticate_user(user, input_password)