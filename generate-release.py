import json
import os
import fnmatch

exclude = ["gtnh-assets", "issue", "mods-versions-wrapper"]
exclude_mods = ["MrTJPCore", "CodeChickenLib"]


def list_json_files(directory):
    json_files = []

    for filename in os.listdir(directory):
        if fnmatch.fnmatch(filename, "*.json"):
            flag = True
            for str in exclude:
                if filename.startswith(str):
                    flag = False
                    break
            if flag:
                json_files.append(filename)

    return json_files


def load(list: list):
    result_client = []
    result_server = []
    for mod in list:
        if mod in exclude_mods:
            continue

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

        if list[mod]["side"] == "BOTH" or list[mod]["side"] == "CLIENT":
            result_client.append(item)
        if list[mod]["side"] == "BOTH" or list[mod]["side"] == "SERVER":
            result_server.append(item)

    return result_client, result_server


def save_forge_file(list: list, file):
    forgemodsjson = {
        "repositoryRoot": "ModsRepository",
        "parentList": None,
        "modRef": [],
    }

    for item in list:
        forgemodsjson["modRef"].append(item["id"])

    with open(file, encoding="utf8", mode="w") as file1:
        json.dump(forgemodsjson, file1, indent=4)
        print(f"Saved file {file}")


if __name__ == "__main__":

    filtered_files = list_json_files(os.getcwd())
    with open("gtnh-assets-wrapper.json", encoding="utf8", mode="r") as file:
        gtnh_assets = json.load(file)["mods"]

    for file in filtered_files:
        try:
            version = None
            with open(file, encoding="utf8", mode="r") as file1:
                version = json.load(file1)

            result_client, result_server = load(version["github_mods"])
            result_client1, result_server2 = load(version["external_mods"])
            result_client.extend(result_client1)
            result_server.extend(result_server2)

            dir = "release/" + version["version"]
            if not os.path.exists(dir):
                os.makedirs(dir)

            with open(f"{dir}/client-{file}", encoding="utf8", mode="w") as file1:
                json.dump(result_client, file1, indent=4)
                print(f"Saved file {dir}/client-{file}")

            with open(f"{dir}/server-{file}", encoding="utf8", mode="w") as file1:
                json.dump(result_server, file1, indent=4)
                print(f"Saved file {dir}/server-{file}")

            save_forge_file(result_client, f"{dir}/Forge-client-{file}")
            save_forge_file(result_server, f"{dir}/Forge-server-{file}")

        except KeyError:
            print(f"file: {file}")
            print(version)
