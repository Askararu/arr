#1
class Flyer:
    def fly(self):
        print("Flying")

class Swimmer:
    def swim(self):
        print("Swimming")

class Duck(Flyer, Swimmer):
    pass

d = Duck()
d.fly()   
d.swim()  

#2
class A:
    def do(self):
        print("A")

class B:
    def do(self):
        print("B")

class C(A, B):
    pass

C().do()  

#3
class X:
    def action(self):
        print("X")

class Y(X):
    def action(self):
        super().action()
        print("Y")

class Z(X):
    def action(self):
        super().action()
        print("Z")

class P(Y, Z):
    def action(self):
        super().action()
        print("P")

P().action()
#4
class A:
    def __init__(self):
        print("A init")

class B:
    def __init__(self):
        print("B init")

class C(A, B):
    def __init__(self):
        super().__init__()
        print("C init")

C()

