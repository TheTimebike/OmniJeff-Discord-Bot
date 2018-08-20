import asyncio, time, threading, queue, discord, sys, os, json
client = discord.Client()

@client.event
async def on_ready():
    print('Debate Module: Logged in as:\n{0} (ID: {0.id})'.format(client.user))
class Vote:
    
    def __init__(self, message):
        self.timeToWait = 60
        self.minConverter = {"h": 3600, "m": 60, "s": 1}
        self.yesVoters = []
        self.noVoters = []
        self.yesTotal = 0
        self.noTotal = 0
        self.targetMessage = message
        self.timer = self.targetMessage.content[self.targetMessage.content.find("[")+len("["):self.targetMessage.content.rfind("]")]
        self.poll = self.targetMessage.content.replace("[{0}]".format(self.timer), " ")
        self.timeToWait = int(self.timer[:-1]) * self.minConverter[self.timer[-1:]]
        print(self.timer)
        print(self.poll)
        print(self.timeToWait)

    def __str__(self):
        return "{0}\n{1} people have voted yes, {2} people have voted no.".format(self.poll, self.yesTotal, self.noTotal)

    def newNoVoter(self, user):
        try:
            if user.id in self.yesVoters:
                self.yesVoters.remove(user.id)
                self.yesTotal -= 1
            self.noVoters.append(user.id)
            self.noTotal += 1
            return True
        except:
            return False

    def newYesVoter(self, user):
        try:
            if user.id in self.noVoters:
                self.noVoters.remove(user.id)
                self.noTotal -= 1
            self.yesVoters.append(user.id)
            self.yesTotal += 1
            return True
        except Exception as ex:
            return ex

    def startTimer(self):
        time.sleep(self.timeToWait)
        self.data = "**THE POLL HAS CONCLUDED!**\n{0}".format(str(self))

dictStorage = {}

@client.event
async def on_reaction_add(reaction, user):
    try:
        if reaction.emoji == "🇾" and user.id != "419504879426600971":
            print(dictStorage[reaction.message.id].newYesVoter(user))
            await client.remove_reaction(reaction.message, "🇳", user)
        if reaction.emoji == "🇳" and user.id != "419504879426600971":
            print(dictStorage[reaction.message.id].newNoVoter(user))
            await client.remove_reaction(reaction.message, "🇾", user)
    except Exception as ex:
        print(ex)
        pass

@client.event
async def on_message(message):
    with open("./servers.config", 'r') as jsonfile:
        modConfig = json.load(jsonfile)
    if message.server.id in modConfig["disabled"]:
        return
    if message.content.lower().startswith("!poll") and message.author.id != "425071640414650379":
        await client.delete_message(message)
        msg = await client.send_message(message.channel, "**Poll starting, please wait.**")
        dictStorage[msg.id] = Vote(message)
        the = threading.Thread(target=dictStorage[msg.id].startTimer).start()
        await client.edit_message(msg, "**POLL STARTED**\n{0}".format(dictStorage[msg.id].poll))
        await client.add_reaction(msg, "🇾")
        await client.add_reaction(msg, "🇳")
        await asyncio.sleep(dictStorage[msg.id].timeToWait)
        await client.send_message(msg.channel, dictStorage[msg.id].data)

client.run(sys.argv[1])