#1
numbers = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x * 2, numbers))
print(doubled)
#2
words = ["apple", "hi", "banana"]
lengths = list(map(lambda x: len(x), words))
print(lengths)  
#3
nums = [2, 4, 6]
squares = list(map(lambda x: x ** 2, nums))
print(squares)  # [4, 16, 36]
#4
celsius = [0, 20, 30]
fahrenheit = list(map(lambda c: c * 9/5 + 32, celsius))
print(fahrenheit)
