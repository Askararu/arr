from functools import reduce
numbers = [1, 2, 3, 4, 5, 6]
squares = list(map(lambda x: x**2, numbers))
print(squares) 
evens = list(filter(lambda x: x % 2 == 0, numbers))
print( evens)
sum_all = reduce(lambda a, b: a + b, numbers)
print(sum_all)  