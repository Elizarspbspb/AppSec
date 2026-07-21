def nod(a, b):
    while True:
        if b == 0:
            return a
        temp = a % b
        a = b
        b = temp

count = int(input())
messages = list(map(int, input().split()))

p = messages[0]

for message in messages:
    p = nod(p, message)

print(p, end=' ')