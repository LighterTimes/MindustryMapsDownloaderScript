import requests as req
import json
import re
import os

if not "wget: missing URL" in os.popen("wget").read():
    print("[0;31mMissing dependencies: Wget[0m\n[0;35m[TIP][0m If you are on windows you can install wget using [0;32mwinget install wget[0m\n If you are on OSX you can get it using [0;32mbrew install wget[0m\nIf you use GNU/Linux than you should know how to install it")
    exit(1)

# put your account token here
token = ""
channel_id = "416719902641225732"

headers = {
    'token' : token
}

print("[0;33m[MMDS][0m made by [0;34mLighterTimes#7613[0m\nReport bugs at: https://github.com/LighterTimes/MindustryMapsDownloaderScript/issues/new")
print("Fletching messages from channel {channel_id}")

# get latest messages
messages = req.get(f"https://discord.com/api/v9/channels/{channel_id}/messages", headers=headers).text
data = json.loads(messages)
last = 0

# Load more and more older messages in batches of 50
while (data[-1]["id"] != last):
    last = data[-1]["id"]
    r = req.get(f"https://discord.com/api/v9/channels/{channel_id}/messages?before={last}&limit=50", headers=headers)
    data += json.loads(r.text)

print(f"Done fletching messages from channel {channel_id}")
print("Extracting [0;33m.msav files from chat logs")

# get all the .msav attachments
results = re.findall(r"https:\/\/cdn\.discordapp\.com\/attachments\/416719902641225732\/[0-9]+\/\w+\.msav", data)

print("Done extracting [0;33m.msav files")

with open("links.txt", "w") as file:
    for link in results:
        file.write(link)

print("Downloading [0;31m{0}[0m maps".format(len(results)))

download = os.popen("wget -i {0}")

print("\n\n[1;33mDone downloading [0;31m{0} [1;33mmaps from channel {1}[0m\n\n".format(len(results), channel_id))