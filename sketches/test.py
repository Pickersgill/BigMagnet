import json
import sys

with open(sys.argv[1]) as src:
    data = json.loads(src.read())


print(data["total_count"])
for item in data["items"]:
    print(item["url"])
    print(item["license"])
    #i = data["items"][0][item]
    #print(i["url"])
    #print(i["license"])

print(len(data["items"]))
