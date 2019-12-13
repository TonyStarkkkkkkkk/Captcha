import random
import sys
# sys.setrecursionlimit(100000)


# lst = []
# while len(lst) <= 100000:
#     lst.append(random.randint(1, 4))
#     for i in range(random.randint(2, 20)):
#         lst.append(0)
# print(lst)
# with open("test.txt", "w") as f:
#     f.write(str(lst))

# with open("test.txt", "r") as file:
#     lst = eval(file.read())
#
#
# def f(x):
#     if x == 2:
#         return 3
#     elif x == 3:
#         return 6
#     else:
#         return 3*f(x-2)+6*g(x-2)
#
#
# def g(x):
#     if x == 2:
#         return 2
#     elif x == 3:
#         return 7
#     else:
#         return 2*f(x-2)+7*g(x-2)


def f(x):
    if x % 2 == 0:
        return int(pow(9, x//2)/4 + 3/4)
    else:
        return 3*f(x-1)-3


def g(x):
    if x % 2 == 0:
        return f(x)-1
    else:
        return f(x)+1


lst = input('plz input:').split(" ")

start, end = 0, 0
for i in range(len(lst)):
    if lst[i] != '0':
        break
    start = start + 1
for j in range(len(lst)-1, 0, -1):
    if lst[j] != '0':
        break
    end = end + 1
temp = lst[start]
step = 1
count = pow(3, start+end)
print('count:', count)
print(start, end)
for i in range(start+1, len(lst)-end):
    if lst[i] != '0':
        if lst[i] == temp:
            print(step)
            count = count*f(step)
            print(f(step))
            step = 1
        else:
            count = count*g(step)
            print(g(step))
            step = 1
        temp = lst[i]
    elif lst[i] == '0':
        step = step + 1

print(count)





