import json


nameMap = {
    "Buildcraft Oil Tweaks": "BuildCraftOilTweak",
    "Gravitation Suite": "GraviSuite",
    "Gravitation-Suite-old": "GraviSuite",
    "Thaumic Machina": "Thaumic-Machina",
    "UniLib": "UniLib",
}


def processMod(gtnh_mods):
    mods = {}
    for mod in gtnh_mods:
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
            elif item["url"].startswith("https://modrinth.com/mod/"):
                name = (
                    item["url"]
                    .removeprefix("https://modrinth.com/mod/")
                    .split("/", 2)[0]
                )
                item["id"] = f"modrinth:{name}:<version>"
                item["src"] = "modrinth"
            elif mod["name"] in nameMap:
                name = nameMap[mod["name"]]
                item["id"] = f"other:{name}:<version>"
                item["src"] = "other"
            else:
                print("Err Mod: ")
                print(mod)
                item["id"] = f"other:{name}:<version>"
                item["src"] = "other"
        mods[mod["name"]] = item

    return mods


def proceesConfig(gtnh_config):
    configs = {}
    config = {}
    config["latest"] = gtnh_config["latest_version"]
    config["url"] = gtnh_config["repo_url"]
    config["versions"] = {}
    for version in gtnh_config["versions"]:
        ver = {}
        ver["name"] = version["filename"]
        ver["url"] = version["browser_download_url"]
        config["versions"][version["version_tag"]] = ver

    configs[gtnh_config["name"]] = config

    return configs


def processModsVersionsFile(mods):
    modsVersons = []
    index = 0
    for modUid in mods:
        modVersionJson = []
        modInfo = mods[modUid]

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

            item["path"] = path + ".jar"

            if "private" in modInfo and modInfo["private"]:
                item["private"] = True

            modVersionJson.append(item)

        modUidStr = modUid.replace(":", "").replace(" ", "-")
        filename = f"version/{'%03d'%index}_{modUidStr}.json"
        with open(filename, encoding="utf8", mode="w") as file:
            json.dump(modVersionJson, file, indent=4)
        index += 1

        item = {}
        item["name"] = modUid
        item["path"] = filename
        item["versions"] = []
        for verStr in modInfo["versions"]:
            item["versions"].append(verStr)

        modsVersons.append(item)

    return modsVersons


if __name__ == "__main__":
    with open("gtnh-assets.json", encoding="utf8", mode="r") as file:
        gtnh_assets = json.load(file)

    result = {}
    result["mods"] = processMod(gtnh_assets["mods"])
    result["config"] = proceesConfig(gtnh_assets["config"])

    with open("gtnh-assets-wrapper.json", encoding="utf8", mode="w") as file:
        json.dump(result, file, sort_keys=True, indent=4)

    modsVersons = processModsVersionsFile(result["mods"])

    with open("mods-versions-wrapper.json", encoding="utf8", mode="w") as file:
        json.dump(modsVersons, file, sort_keys=True, indent=4)
