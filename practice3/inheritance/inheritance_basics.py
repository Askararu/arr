#1
class Animal:
    def speak(self):
        print("Some sound")

class Dog(Animal):
    pass

dog = Dog()
dog.speak()  

#2
class Cat(Animal):
    def meow(self):
        print("Meow")

cat = Cat()
cat.speak()  
cat.meow()   

#3
class Bird(Animal):
    def __init__(self, name):
        self.name = name

bird = Bird("Parrot")
print(bird.name)  

#4
class Mammal(Animal):
    def feed_milk(self):
        print("Feeding milk")

class Human(Mammal):
    def speak(self):
        print("Hello")

h = Human()
h.feed_milk()
h.speak()      
