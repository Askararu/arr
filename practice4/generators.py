#1
def sqr(n):
    for i in range(n+1):
        yield i*i
for x in sqr(10):
    print(x)
#2
def even(n):
    for i in range(n+1):
        if i%2==0:
            yield i
n = int(input())

print(",".join(str(num) for num in even(n)))
#3
def div(n):
    for i in range(n+1):
        if i%3==0 and i%4==0:
            yield i
for x in div(72):
    print(x)
#4
sq = (x*x for x in range(1, 6))
for i in sq:
    print(i)
#5
def count(n):
    for i in range(n, -1, -1):
        yield i


for x in count(5):
    print(x)