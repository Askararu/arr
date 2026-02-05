#1
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  if x == "banana":
    continue
  print(x)
#2
for i in range(1, 6):
    if i == 3:
        continue
    print(i)

#2
for i in range(1, 6):
    if i % 2 == 0:
        continue
    print(i)

#3
for letter in "hi there":
    if letter == " ":
        continue
    print(letter)

#4
nums = [1, -2, 3, -4, 5]
for n in nums:
    if n < 0:
        continue
    print(n)