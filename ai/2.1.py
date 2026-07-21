import re

n = int(input())
half = []
for i in range(n):
    stroka = str(input())
    half.append(stroka)
    
digit = 0

for i in half:
#for x in range(i):
#for x in i:
    #stroka = str(input())
    #for symbol in stroka:
    for symbol in i:
        if not (symbol.isdigit() or symbol == " " or symbol == "-" or symbol == "\t"):
            print("INVALID2")
            digit = 1
            break
    if digit == 1:
        digit = 0
        continue
    #numbers = list(map(int, re.split(r'[\t -]+', stroka)))
    stroka = stroka.replace(" ", "")
    stroka = stroka.replace("\t", "")
    stroka = stroka.replace("-", "")
    numbers = [int(char) for char in stroka]
    double = False
    luna = 0
    for num in reversed(numbers):
        if double:
            num *= 2
            if num > 9:
                num -= 9
            double = False
        else:
            double = True
        luna += num
        
    if luna % 10 == 0:
        print("token = ", num)
        print("VALID")
    else:
        print("INVALID")