import json
import os
import shutil

mods_list_file = "2.6.1.json"
mods_repository = "../ModsRepository"


def moveFile(source_file, destination_file):
    target = os.path.abspath(os.path.join(mods_repository, destination_file))
    dirname = target.removesuffix(target.split(os.sep)[-1])
    os.makedirs(dirname)
    shutil.move(source_file, target)


with open(mods_list_file, encoding="utf8", mode="r") as file:
    modsListJson = json.load(file)

nameToObject = {}

for item in modsListJson:
    nameToObject[item["filename"]] = item

ForgeModsListFile = {
    "modRef": [],
    "repositoryRoot": mods_repository.removeprefix("../"),
    "parentList": None,
}

for file in os.listdir():
    if file.endswith(".jar"):
        if file in nameToObject:
            moveFile(file, nameToObject[file]["path"])
            ForgeModsListFile["modRef"].append(nameToObject[file]["id"])

with open(f"Forge-{mods_list_file}", encoding="utf8", mode="w") as file:
    json.dump(ForgeModsListFile, file, indent=4, sort_keys=True)
