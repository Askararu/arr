# the expression is evaluated and Python returns the Boolean answer:
print(10 > 9)
print(10 == 9)
print(10 < 9)
#Evaluate a string and a number:
print(bool("Hello"))
print(bool(15))
#Any list, tuple, set, and dictionary are True, except empty ones.
bool("abc")
bool(123)
bool(["apple", "cherry", "banana"])
#The following will return False:
bool(False)
bool(None)
bool(0)
bool("")
bool(())
bool([])
bool({})
#We can create functions that returns a Boolean Value
def myFunction() :
  return True

print(myFunction())
