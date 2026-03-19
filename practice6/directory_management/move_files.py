import os
import shutil

os.makedirs("kitchen", exist_ok=True)
os.makedirs("fridge", exist_ok=True)

with open("kitchen/ice_cream.txt", "w") as f:
    f.write("vanilla ice cream")

shutil.copy("kitchen/ice_cream.txt", "fridge/ice_cream_copy.txt")
shutil.move("kitchen/ice_cream.txt", "fridge/ice_cream_moved.txt")

print(os.listdir("fridge"))