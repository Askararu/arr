#1
class Person:
    def __init__(self, name):
        self.name = name

class Student(Person):
    def __init__(self, name, grade):
        super().__init__(name)
        self.grade = grade

s = Student("Alice", 10)
print(s.name, s.grade)  

#2
class Vehicle:
    def start(self):
        print("Vehicle started")

class Car(Vehicle):
    def start(self):
        super().start()
        print("Car engine on")

c = Car()
c.start()
#3
class A:
    def greet(self):
        print("Hello from A")

class B(A):
    def greet(self):
        super().greet()
        print("Hello from B")

class C(B):
    def greet(self):
        super().greet()
        print("Hello from C")

C().greet()
#4
class Base:
    def __str__(self):
        return "Base class"

class Child(Base):
    def __str__(self):
        return super().__str__() + " -> Child class"

print(Child())  

