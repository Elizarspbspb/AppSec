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
        print("Итерация номер:", i)
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