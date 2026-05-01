import os
from functools import reduce
from collections import defaultdict

#1
folder_name = "sales"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)


file_data = {
    "store1.txt": "Laptop,3\nMouse,10\nKeyboard,5\n",
    "store2.txt": "Monitor,2\nHeadphones,4\nLaptop,2\n",
    "store3.txt": "Mouse,2\nKeyboard,8\nWebcam,1\n"
}

for filename, content in file_data.items():
    with open(os.path.join(folder_name, filename), "w") as f:
        f.write(content)

#2
products = []
files = os.listdir(folder_name)

for file in files:
    with open(os.path.join(folder_name, file), "r") as f:
        for line in f:
            if line.strip():
                name, qty = line.strip().split(",")
                products.append((name, int(qty)))


sales_sum = defaultdict(int)
for name, qty in products:
    sales_sum[name] += qty

products_summed = [(name, qty) for name, qty in sales_sum.items()]

#3
total_records = len(products_summed)
quantities = [qty for _, qty in products_summed]
total_qty = sum(quantities)
avg_qty = total_qty / total_records if total_records else 0
max_sale = max(quantities) if quantities else 0
min_sale = min(quantities) if quantities else 0
increased_products = list(map(lambda p: (p[0], p[1]+2), products_summed))
popular_products = list(filter(lambda p: p[1] > 5, products_summed))
product_of_all = reduce(lambda x, y: x*y, quantities, 1)

names_list = [p[0] for p in products_summed]
zipped_data = list(zip(names_list, quantities))
sorted_products = sorted(products_summed, key=lambda x: x[1], reverse=True)

#4
with open("sales_report.txt", "w") as report:
    report.write(f"Total records: {total_records}\n")
    report.write(f"Average quantity sold: {avg_qty:.1f}\n")
    report.write(f"Highest quantity sold: {max_sale}\n")
    report.write(f"Lowest quantity sold: {min_sale}\n\n")
    report.write("Popular products:\n")
    for name, qty in popular_products:
        report.write(f"{name} {qty}\n")

#5
for index, (name, qty) in enumerate(products_summed, start=1):
    print(f"{index} {name} {qty}")

