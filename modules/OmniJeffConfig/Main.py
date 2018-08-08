import discord, sys, os, json
client = discord.Client()

@client.event
async def on_message(message):
    if message.content.lower().startswith("!config see"):
        configPortfolio = "Config for {0}".format(message.server.name)
        moduleList = next(os.walk('../modules/'))[1]
        for directory in moduleList:
            with open("../modules/{0}/servers.config".format(directory), 'r') as jsonfile:
                modConfig = json.load(jsonfile)
            if message.server.id in modConfig["disabled"]:
                configPortfolio += "\n {0}: Disabled".format(directory)
            else:
                configPortfolio += "\n {0}: Enabled".format(directory)
        print(configPortfolio)
        await client.send_message(message.channel, configPortfolio)
    if message.content.lower().startswith("!config enable"):
        configToEdit = message.content.lower()[15:]
        with open("../{0}/server.config".format(configToEdit), 'r') as jsonfile:
            serverConfig = json.load(jsonfile)
        if message.server.id not in serverConfig["disabled"]:
            await client.send_message(message.channel, "This module is already enabled")
        else:
            serverConfig["disabled"].remove(message.server.id)
            await client.send_message(message.channel, "This module has been enabled")
        with open("../{0}/server.config".format(configToEdit), 'w') as outfile:
            json.dump(data, outfile)
    if message.content.lower().startswith("!config disable"):
        configToEdit = message.content.lower()[16:]
        with open("../{0}/server.config".format(configToEdit), 'r') as jsonfile:
            serverConfig = json.load(jsonfile)
        if message.server.id in serverConfig["disabled"]:
            await client.send_message(message.server, "This module is already disabled")
        else:
            serverConfig["disabled"].append(message.server.id)
            await client.send_message(message.channel, "This module has been disabled")
        with open("../{0}/server.config".format(configToEdit), 'w') as outfile:
            json.dump(data, outfile)
client.run(sys.argv[1])