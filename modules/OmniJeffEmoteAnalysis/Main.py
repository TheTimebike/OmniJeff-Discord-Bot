import discord, os, sys, json
client = discord.Client()

@client.event
async def on_ready():
    print('Emote Analysis Module: Logged in as:\n{0} (ID: {0.id})'.format(client.user))



client.run(sys.argv[1])