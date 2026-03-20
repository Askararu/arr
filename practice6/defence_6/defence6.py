import os
from functools import reduce

#1
folder = "sales"
if not os.path.exists(folder):
    os.makedirs(folder)

file_data = {
    "store1.txt": "Laptop,3\nMouse,10\nKeyboard,5\n",
    "store2.txt": "Monitor,2\nHeadphones,4\nLaptop,2\n",
    "store3.txt": "Mouse,2\nKeyboard,8\nWebcam,1\n"
}

for filename, content in file_data.items():
    with open(os.path.join(folder, filename), "w") as f:
        f.write(content)

#2
products = []
files = os.listdir(folder)

for file in files:
    with open(os.path.join(folder, file), "r") as f:
        for line in f:
            if line.strip():
                name, qty = line.strip().split(",")
                products.append((name, int(qty)))

#3
total_records = len(products)
quantities = [p[1] for p in products]
total_qty = sum(quantities)
max_sale = max(quantities)
min_sale = min(quantities)
increased = list(map(lambda x: x + 2, quantities))
popular = list(filter(lambda p: p[1] > 5, products))
product_all = reduce(lambda x, y: x * y, quantities)

names_list = [p[0] for p in products]
zipped = list(zip(names_list, quantities))
sorted_prod = sorted(products, key=lambda x: x[1], reverse=True)
avg = total_qty / total_records if total_records > 0 else 0

#4
with open("sales_report.txt", "w") as report:
    report.write(f"Total records: {total_records}\n")
    report.write(f"Average quantity sold: {avg:.1f}\n")
    report.write(f"Highest quantity sold: {max_sale}\n")
    report.write(f"Lowest quantity sold: {min_sale}\n\n")
    report.write("Popular products:\n")
    for name, qty in popular:
        report.write(f"{name} {qty}\n")

#5
for index, (name, qty) in enumerate(products, start=1):
    print(f"{index} {name} {qty}")

