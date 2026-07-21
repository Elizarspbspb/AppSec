from collections import Counter

def is_prime(n):
    if n == 1:
        return 0
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n and n % d != 0:
        d += 2
    return d * d > n
    
def find_duplicates(nums, n):
    counts = Counter(nums)
    result = []
    for item, count in counts.items():
        if count == n:
            return item
    
# Первая строка: одно целое число
n = int(input())

# Вторая строка: несколько целых чисел через пробел
numbers = list(map(int, input().split()))
easy_mas = []

if len(numbers) != n:
    print("Ошибка: количество чисел не совпадает")
else:
    for num in numbers:
        half = []
        for i in range(1, num+1):
            if num % i == 0:
                half.append(i)
        for x in half:
            if is_prime(x):
                easy_mas.append(x)
    print(find_duplicates(easy_mas, n), end=" ")