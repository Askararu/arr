#1
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  print(x)
  if x == "banana":
    break
#2
for i in range(1, 6):
    if i == 3:
        break
    print(i)

#3
numbers = [1, 3, 5, 6, 7]
for n in numbers:
    if n % 2 == 0:
        print(n)
        break

#4
for letter in "abcdef":
    if letter == 'c':
        break
    print(letter)

#5
nums = [5, 3, 2, -1, 4]
for n in nums:
    if n < 0:
        print("Found:", n)
        break