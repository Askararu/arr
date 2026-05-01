import json

data = '''
{
  "class": {
    "group": "A1",
    "students": [
      {"name": "Ann", "scores": [80, 90, 85]},
      {"name": "Tom", "scores": [70, 75, 72]},
      {"name": "Kate", "scores": [95, 92, 93]}
    ]
  }
}
'''
obj = json.loads[data]
bav = 0
best = []
for person in obj["class"]["students"]:
    av = sum(person["scores"])
