#import numpy as np
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
    # Возвращает ключи, которые встречаются больше 1 раза
    #return [item for item, count in counts.items() if count > 1]
    #return [item for item, count in counts.items() if count == n]
    result = []
    for item, count in counts.items():
        if count == n:
            #result.append(item)
            return item
    
# Первая строка: одно целое число
n = int(input())

# Вторая строка: несколько целых чисел через пробел
numbers = list(map(int, input().split()))
# half = []
easy_mas = []
easy = 0
#my_numpy = np.array([])

if len(numbers) != n:
    print("Ошибка: количество чисел не совпадает.")
else:
    for num in numbers:
        #print("num = ", num)
        half = []
        for i in range(1, num+1):
            #print("i = ", i)
            if num % i == 0:
                print(i, end=" ")
                half.append(i)
        print(" ")
        for x in half:
            if is_prime(x):
                print(x, end=' ')
                easy_mas.append(x)
                #if x not in easy_mas:
                #    easy_mas.append(x)
                #else: 
                #    easy = x
        print("-------------")
    print("=============")
    for x in easy_mas:
        print(x, end=' ')
    print()
    #print(find_duplicates([1, 2, 3, 4, 2, 3, 3]))  # Выведет: [2, 3]
    print(find_duplicates(easy_mas, n))  # Выведет: [2, 3]
    #print("easy = ", easy)