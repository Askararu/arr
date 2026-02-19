#1
students = [("Emil", 25), ("Tobias", 22), ("Linus", 28)]
sorted_students = sorted(students, key=lambda x: x[1])
print(sorted_students)
#2
words = ["apple", "pie", "banana", "cherry"]
sorted_words = sorted(words, key=lambda x: len(x))
print(sorted_words)
#3
words = ["cat", "banana", "apple"]
result = sorted(words, key=lambda x: x[-1])
print(result)
#4
pairs = [(1, 3), (2, 1), (4, 2)]
result = sorted(pairs, key=lambda x: x[1])
print(result)
