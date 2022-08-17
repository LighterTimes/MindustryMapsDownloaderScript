from shutil import which
import requests as req
import json
import re
import os

if which("wget") is None:
    print("[0;31mMissing dependencies: Wget[0m\n[0;35m[TIP][0m If you are on windows you can install wget using [0;32mwinget install wget[0m\nIf you are on OSX you can get it using [0;32mbrew install wget[0m\nIf you use GNU/Linux than you should know how to install it")
    exit(1)


# put your account token here
token = ""
channel_id = "416719902641225732" #maps = 416719902641225732 --- #schematics = 640604827344306207
target = "msav" # msav = map/save file --- msch = schematic #

print("[0;33m[MMDS][0m made by [0;36mLighterTimes#7613[0m\n[0;32m[D][0m Report bugs at: [4;34mhttps://github.com/LighterTimes/MindustryMapsDownloaderScript/issues/new[0m")
print(f"[0;36m[I][0m Fletching messages from channel {channel_id}")

# get latest messages
headers = {
    "authorization" : token
}

r = req.get(f"https://discord.com/api/v9/channels/{channel_id}/messages", headers=headers)
data = json.loads(r.text)
last = 0

# Load more and more older messages in batches of 50
while (data[-1]["id"] != last):
    last = data[-1]["id"]
    print("[0;32m[D][0m Fletching messages from around" + str(data[-1]['timestamp'])[0:10])
    r = req.get(f"https://discord.com/api/v9/channels/{channel_id}/messages?before={last}&limit=50", headers=headers)
    data += json.loads(r.text)

print(f"[0;36m[I][0m Done fletching messages from channel {channel_id}")
print(f"[0;36m[I][0m Extracting [0;33m.{target} files from chat logs")

# get all the .{target} attachments
results = re.findall(re("https:\/\/cdn\.discordapp\.com\/attachments\/{0}\/[0-9]+\/\w+\.{1}".format(channel_id, target)), data)

print(f"[0;36m[I][0m Done extracting [0;33m.{target} files")

with open("links.txt", "w") as file:
    for link in results:
        file.write(link)

print("[0;36m[I][0m Downloading [0;31m{0}[0m .{1} files".format(len(results), target))

download = os.popen("wget --no-verbose -i links.txt")
print(download.read())

print("\n\n[1;33mDone downloading [0;31m{0} [1;33m.{1} files from channel {2}[0m\n\n".format(len(results), target, channel_id))