# in json file store sides of regraingler you should find piremeter of rectaingeler and devide it by 3 and get ceil vaule with math module write the result to another json file
import json 
import math 
with open("re.json","r") as f:
    data = json.load(f)
a = data["a"]
b = data["b"]
p = (a+b)*2
result = math.ceil(p/3)
output = {
    "result": result
}
with open("output.json","w") as f:
    json.dump(output,f,indent=4)