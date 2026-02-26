class Product:
    total_products = 0  

    def __init__(self, name, price):
        self.name = name
        self.price = price
        Product.total_products += 1

    def get_info(self):
        return f"Name: {self.name}, Price: {self.price}"

    @classmethod
    def get_total_products(cls):
        return cls.total_products


class DigitalProduct(Product):
    def __init__(self, name, price, file_size):
        super().__init__(name, price)
        self.file_size = file_size

    def get_info(self):
        return f"{super().get_info()}, File size: {self.file_size}"


class PhysicalProduct(Product):
    def __init__(self, name, price, weight):
        super().__init__(name, price)
        self.weight = weight

    def get_info(self):
        return f"{super().get_info()}, Weight: {self.weight}"


p1 = DigitalProduct("choco", 10, 5)
p2 = PhysicalProduct("cake", 1000, 2.5)

print(p1.get_info())
print(p2.get_info())

print("Total products:", Product.get_total_products())