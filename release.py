import json
import os
import fnmatch


def list_json_files(directory):
    json_files = []

    for filename in os.listdir(directory):
        if fnmatch.fnmatch(filename, "*.json"):
            if not filename.startswith("gtnh-assets-wrapper"):
                json_files.append(filename)

    return json_files


filtered_files = list_json_files(os.getcwd())


def load(list: list):
    result = []
    for mod in list:
        if list[mod]["side"] == "BOTH" or list[mod]["side"] == "CLIENT":
            modInfo = gtnh_assets[mod]
            verStr = list[mod]["version"]
            ver = modInfo["versions"][verStr]
            item = {}
            item["id"] = modInfo["id"].replace("<version>", verStr)
            item["uid"] = mod
            item["filename"] = ver["name"]
            item["url"] = ver["url"]

            group = item["id"].split(":")
            path = (
                group[0].replace(".", "/")
                + "/"
                + group[1]
                + "/"
                + group[2]
                + "/"
                + group[1]
                + "-"
                + group[2]
            )
            if len(group) == 4:
                path = path + "-" + group[4]
            path += ".jar"
            item["path"] = path

            if "private" in modInfo and modInfo["private"]:
                item["private"] = True

            result.append(item)

    return result


with open("gtnh-assets-wrapper-formatted.json", encoding="utf8", mode="r") as file:
    gtnh_assets = json.load(file)["mods"]

for file in filtered_files:
    version = None
    with open(file, encoding="utf8", mode="r") as file1:
        version = json.load(file1)

    result = load(version["github_mods"])
    result.extend(load(version["external_mods"]))

    with open(f"release/{file}", encoding="utf8", mode="w") as file1:
        json.dump(result, file1, indent=4)
        print(f"Saved file release/{file}")

    forgemodsjson = {
        "repositoryRoot": "ModsRepository",
        "parentList": None,
        "modRef": [],
    }

    for item in result:
        forgemodsjson["modRef"].append(item["id"])

    with open(f"release/Forge-{file}", encoding="utf8", mode="w") as file1:
        json.dump(forgemodsjson, file1, indent=4)
        print(f"Saved file release/Forge-{file}")
