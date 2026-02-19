#1
class Animal:
    def speak(self):
        print("Some sound")

class Dog(Animal):
    def speak(self):
        print("Woof")

Dog().speak()  

#2
class Parent:
    def show(self):
        print("Parent show")

class Child(Parent):
    def show(self):
        super().show()
        print("Child show")

Child().show()
#3
class Person:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return f"Person: {self.name}"

class Student(Person):
    def __str__(self):
        return f"Student: {self.name}"

print(Student("Bob"))  

#4
class Shape:
    def area(self):
        return 0

class Square(Shape):
    def __init__(self, side):
        self.side = side
    def area(self):
        return self.side ** 2

print(Square(5).area())  
