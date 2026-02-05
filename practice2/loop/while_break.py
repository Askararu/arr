#1 Exit the loop when i is 3:
i = 1
while i < 6:
  print(i)
  if i == 3:
    break
  i += 1
#2 Stop if user types 'no'
while True:
    answer = input("Type 'no' to stop: ")
    if answer == "no":
        break
    print("You typed:", answer)
#3 Stop if sum > 5
sum_num = 0
i = 1
while True:
    sum_num += i
    if sum_num > 5:
        break
    print(sum_num)
    i += 1