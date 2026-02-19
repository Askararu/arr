#1
class Student:
    total_students = 0   

    def __init__(self, name):
        self.name = name
        Student.total_students += 1


s1 = Student("Aida")
s2 = Student("Ali")

print(Student.total_students)  
#2
class Product:
    tax = 0.2  

    def __init__(self, price):
        self.price = price

    def final_price(self):
        return self.price * (1 + Product.tax)


p1 = Product(100)
p2 = Product(200)

print(p1.final_price())  
print(p2.final_price())  
#3
class Student:
    university = "KBTU"

    def __init__(self, name):
        self.name = name


s1 = Student("Dana")
s2 = Student("Arman")

print(s1.university)  
print(s2.university)  

#4
class Car:
    wheels = 4

    def __init__(self, model):
        self.model = model


c1 = Car("Toyota")
Car.wheels = 6

print(c1.wheels)  
