import json

with open("../results/mini.json") as raw:
    data = json.loads(raw.read())

out = open("mini.urls", "w+")
for d in data:
    out.write(d["url"] + "\n")

out.close()

