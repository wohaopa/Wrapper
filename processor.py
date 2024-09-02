import json
import os

gtnh_assets = None
nameMap = {
    "Buildcraft Oil Tweaks": "BuildCraftOilTweak",
    "Gravitation Suite": "GraviSuite",
    "Gravitation-Suite-old": "GraviSuite",
    "Thaumic Machina": "Thaumic-Machina",
    "UniLib": "UniLib",
}


with open("gtnh-assets.json", encoding="utf8", mode="r") as file:
    gtnh_assets = json.load(file)


mods = gtnh_assets["mods"]
Mods = {}
for mod in mods:
    item = {}
    item["latest"] = mod["latest_version"]
    if "private" in mod and mod["private"]:
        item["private"] = True

    vers = {}
    for version in mod["versions"]:
        ver = {}
        ver["name"] = version["filename"]
        if version["download_url"].startswith("https://api.github.com/repos/"):
            ver["url"] = version["browser_download_url"]
        else:
            ver["url"] = version["download_url"]

        vers[version["version_tag"]] = ver

    item["versions"] = vers
    if "repo_url" in mod:
        item["url"] = mod["repo_url"]
    elif "external_url" in mod:
        item["url"] = mod["external_url"]
    else:
        item["url"] = "<unknown>"

    if item["url"].startswith("https://github.com/GTNewHorizons/"):
        name = mod["name"]
        item["id"] = f"com.github.GTNewHorizons:{name}:<version>"
        item["src"] = "GTNH"
    elif item["url"].startswith("https://github.com/"):
        group = item["url"].removeprefix("https://github.com/").split("/", 3)
        item["id"] = f"com.github.{group[0]}:{group[1]}:<version>"
        item["src"] = "github"
    else:
        name = "<unknown>"
        if item["url"].startswith("https://www.curseforge.com/minecraft/mc-mods/"):
            name = (
                item["url"]
                .removeprefix("https://www.curseforge.com/minecraft/mc-mods/")
                .split("/", 2)[0]
            )
            item["id"] = f"curseforge:{name}:<version>"
            item["src"] = "curse"
        elif mod["name"] in nameMap:
            name = nameMap[mod["name"]]
            item["id"] = f"other:{name}:<version>"
            item["src"] = "other"
    Mods[mod["name"]] = item

Config = {}
gtnh_config = gtnh_assets["config"]
config = {}
config["latest"] = gtnh_config["latest_version"]
config["url"] = gtnh_config["repo_url"]
config["versions"] = {}
for version in gtnh_config["versions"]:
    ver = {}
    ver["name"] = version["filename"]
    ver["url"] = version["browser_download_url"]
    config["versions"][version["version_tag"]] = ver

Config[gtnh_config["name"]] = config

result = {}
result["mods"] = Mods
result["config"] = Config

with open("gtnh-assets-wrapper.json", encoding="utf8", mode="w") as file:
    json.dump(result, file, sort_keys=True, indent=4)

for modUid in Mods:
    modVersionJson = []
    modInfo = Mods[modUid]

    for verStr in modInfo["versions"]:
        item = {}
        item["id"] = modInfo["id"].replace("<version>", verStr)
        item["uid"] = modUid
        item["filename"] = modInfo["versions"][verStr]["name"]
        item["url"] = modInfo["versions"][verStr]["url"]

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

        modVersionJson.append(item)
    with open(f"version/{modUid}.json", encoding="utf8", mode="w") as file:
        json.dump(modVersionJson, file, sort_keys=True, indent=4)
