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