import json

with open("issue.json", encoding="utf8", mode="r") as file:
    iusse = json.load(file)

with open("urls.txt", encoding="utf8", mode="w") as file:
    file.write(iusse["body"])

print("urls:")
print(iusse["body"])
