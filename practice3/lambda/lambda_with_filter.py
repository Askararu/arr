#1
numbers = [1, 2, 3, 4, 5, 6, 7, 8]
odd_numbers = list(filter(lambda x: x % 2 != 0, numbers))
print(odd_numbers)
#2
nums = [5, 12, 8, 20]
big = list(filter(lambda x: x > 10, nums))
print(big)  
#3
words = ["cat", "house", "pen", "notebook"]
long_words = list(filter(lambda x: len(x) > 3, words))
print(long_words)
#4
nums = [-3, 5, -1, 8]
positive = list(filter(lambda x: x > 0, nums))
print(positive)  
