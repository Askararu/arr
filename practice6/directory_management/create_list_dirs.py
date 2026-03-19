import os

os.makedirs("milk/ice_cream/cream", exist_ok=True)

print(os.listdir("."))

py_files = [f for f in os.listdir(".") if f.endswith(".py")]
print(py_files)