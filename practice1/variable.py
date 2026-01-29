#Python has no command for declaring a variable
x = 17
y = "Aru"
print(x)
print(y)

#casting
x = str(17)    # x will be '17'
y = int(19)    # y will be 19
z = float(5)  # z will be 5.0

#We can get the data type of a variable with the type() function
x = 17
y = "Aru"
print(type(x))
print(type(y))

#A will not overwrite a
a = 17
A = "Aru"

#Legal variable names
myvar = "Aru"
my_var = "Aru"
_my_var = "Aru"
myVar = "Aru"
MYVAR = "Aru"
myvar2 = "Aru"

#we can assign values to multiple variables in one line
x, y, z = "pink", "white", "black"
print(x)
print(y)
print(z)

#we can assign the same value to multiple variables in one line
x = y = z = "pink"
print(x)
print(y)
print(z)

#Unpack a Collection
colors = ["pink","white","black"]
x , y , z = colors
print(x)
print(y)
print(z)

#output multiple variables
x = 17
y = "Aru"
print(x,y)

#Global Variables
def myfunc():
  global x
  x = "cool"

myfunc()

print("Cool cool  " + x)

#ex2 
x = "awesome"

def myfunc():
  x = "cool"
  print("Python is " + x)

myfunc()

print("Python is " + x)

#If we use the global keyword, the variable belongs to the global scope
def myfunc():
  global x
  x = "cool"

myfunc()

print("cool cool " + x)