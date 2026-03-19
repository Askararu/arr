with open("choco.txt","r") as file:
    content = file.read
    print(content)
with open("choco.txt", "a") as file:
    file.write("This is new line.\n")
    file.write("That is also new line.\n")
with open("choco.txt","r") as file:
    print(file.read())