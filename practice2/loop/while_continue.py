#1 Continue to the next iteration if i is 3:
i = 0
while i < 6:
  i += 1
  if i == 3:
    continue
  print(i)
#2
i = 1
while i <= 10:
    if i % 2 == 0:
        i += 1
        continue
    print(i)
    i += 1

#3 Skip empty input
i = 0
while i < 5:
    text = input("Enter text: ")
    i += 1
    if text == "":
        continue
    print("You entered:", text)

#4 Skip numbers less than 3
i = 0
while i < 6:
    i += 1
    if i < 3:
        continue
    print(i)

#5 Skip negative numbers
nums = [3, -1, 5, -2, 7]
i = 0
while i < len(nums):
    if nums[i] < 0:
        i += 1
        continue
    print(nums[i])
    i += 1