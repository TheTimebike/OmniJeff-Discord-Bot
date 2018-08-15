import discord, json, sys, os
client = discord.Client()

@client.event
async def on_message(message):
    prefix = "!omnijeff".lower()
    for emote in message.server.emojis:
        if "<:{0.name}:{0.id}>".format(emote) in message.content:
            with open('../serverdata/moduledata/OmniJeffEmoteTracker/{0}.txt'.format(message.server.id), 'r') as inwardFile:
                emoteData = json.load(inwardFile)
            try:
                emoteData["<:{0.name}:{0.id}>".format(emote)] += 1
            except Exception as ex:
                emoteData["<:{0.name}:{0.id}>".format(emote)] = 1
    print(emoteData)
    with open('../serverdata/moduledata/OmniJeffEmoteTracker/{0}.txt'.format(message.server.id), 'w+') as outwardFile:
        json.dump(emoteData, outwardFile, indent=4)

client.run(sys.argv[1])