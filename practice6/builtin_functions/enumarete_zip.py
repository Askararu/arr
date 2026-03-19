chocolate = ["white", "dark", "milk"]
prices = [100, 200, 150]

for idx, choco in enumerate(chocolate):
    print(f"{idx}: {choco}")

for choco, price in zip(chocolate, prices):
    print(f"{choco} costs {price}")