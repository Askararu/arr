#1
def fun(flavor):
    print(flavor ,"milk")
fun("chocolate")
fun("strawberry")
fun("banana")
#2
def my_function(name): 
  print("Hello", name)

my_function("Aru") 
#3
def agein10years(age):
    print(age + 5)

agein10years(17)
#4
def my_function(name = "ice-cream"):
  print("Hello", name)

my_function("choco")
my_function("berry")
my_function()
#5
def my_function(fruits):
  for fruit in fruits:
    print(fruit)

my_fruits = ["apple", "banana", "cherry"]
my_function(my_fruits)