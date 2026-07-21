n = int(input())

tokens = []

for i in range(n):
    tokens.append(input())

for token in tokens:
    token = token.replace("-", "")
    token = token.replace(" ", "")
    
    if token == "" or not token.isdigit():
        print("INVALID")
        continue

    luna = 0
    double = False

    for digit in reversed(token):
        number = int(digit)
        if double:
            number *= 2
            if number > 9:
                number -= 9
        luna += number
        double = not double

    if luna % 10 == 0:
        print("VALID")
    else:
        print("INVALID")