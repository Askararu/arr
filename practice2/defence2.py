products = {
"choco" :500,
"ice-cream" : 250,
"strawberry" : 1000,
"book" : 2250
}
sum = 0
for pro ,price in products.items():
    print(pro,price)
    sum += price
print(sum)