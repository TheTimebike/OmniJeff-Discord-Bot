import discord, json, asyncio, sys, os
client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as:\n{0} (ID: {0.id})'.format(client.user))

@client.event
async def on_raw_message_delete(payload):
    os.remove('./{0}/{1}.txt'.format(payload.guild_id, payload.message_id))

@client.event
async def on_message(message):
    try:
        if message.author.id == client.user.id:
            return
        if message.content.lower().startswith('!rstart'):
            if not message.channel.permissions_for(message.author).manage_roles and message.author.id != 261926271892717569:
                return
            messageID, messageSever, messageOwnership = message.content[8:], message.guild, message.author.id
            for channelT in message.guild.channels:
                try:
                    messageObj = await channelT.get_message(message.content[8:])
                except:
                    foundSomething = False
                    pass
                else:
                    foundSomething = True
                    break
            if not foundSomething:
                await message.channel.send('This is not a valid message ID, please try again with a valid one.')
                return
            await message.channel.send('You have started a setup on the message ' + messageID)
            await message.channel.send('Please use !rrole add (Emote)-(Name of the role), !rnick add (Emote)-(Name to be added) or !rfinish to end')
            newData = {'ownershipSet': [messageOwnership], 'allRoles': [], 'allReactions': [], 'nameStuff': {'allNames': [], 'allReactions': []}}
            def pred(m):
                return m.author == message.author and m.channel == message.channel
            while True:
                foundMessage = await client.wait_for('message', check=pred)
                if foundMessage.content.lower().startswith('!rfinish'):
                    await message.channel.send('Setup finished')
                    if not os.path.exists('./{0}/'.format(message.guild.id)):
                        os.makedirs('./{0}/'.format(message.guild.id))
                    with open('./{0}/{1}.txt'.format(message.guild.id, message.content[8:]), 'w+') as outfile:
                        json.dump(newData, outfile, indent=4)
                    break
                elif foundMessage.content.lower().startswith('!rrole add'):
                    chosenEmote, chosenRole = foundMessage.content[11:].split('-')[0], foundMessage.content[11:].split('-')[1]
                    if chosenRole.lower() == 'none':
                        newData[chosenEmote] = chosenNick
                        newData['allReactions'].append(chosenEmote)
                        await messageObj.add_reaction(chosenEmote[2:-1])
                    else:
                        newData['allReactions'].append(chosenEmote)
                        newData['allRoles'].append(chosenRole)
                        newData[chosenEmote] = chosenRole 
                        await messageObj.add_reaction(chosenEmote[2:-1])
                elif foundMessage.content.lower().startswith('!rnick add'):
                    chosenEmote, chosenNick = foundMessage.content[11:].split('-')[0], foundMessage.content[11:].split('-')[1]
                    if chosenNick.lower() == 'none':
                        newData['nameStuff'][chosenEmote] = chosenNick
                        newData['nameStuff']['allReactions'].append(chosenEmote)
                        await messageObj.add_reaction(chosenEmote[2:-1])
                    else:
                        newData['nameStuff'][chosenEmote] = chosenNick
                        newData['nameStuff']['allReactions'].append(chosenEmote)
                        newData['nameStuff']['allNames'].append(chosenNick)
                        await messageObj.add_reaction(chosenEmote[2:-1])
                else:
                    await message.channel.send('Unexpected input, if you are trying to exit, please use !rfinish')
        if message.content.lower().startswith('!redit'):
            print(message.content[7:])
            if not os.path.isfile('./{0}/{1}.txt'.format(message.guild.id, message.content[7:])):
                return
            with open('./{0}/{1}.txt'.format(message.guild.id, message.content[7:]), 'r') as editFile:
                changingData = json.load(editFile)
            if message.author.id not in changingData['ownershipSet']:
                await message.channel.send('You do not have ownership of this file')
                return
            for channelT in message.guild.channels:
                try:
                    messageObj = await channelT.get_message(message.content[7:])
                except:
                    foundSomething = False
                    pass
                else:
                    foundSomething = True
                    break
            if not foundSomething:
                await message.channel.send('This is not a valid message ID, please try again with a valid one.')
                return
            await message.channel.send('Config file opened for editing')
            await message.channel.send('Please use !rrole add or !rrole remove to add or remove a reaction, or !rnick add and !rnick remove to add or remove a nickname. Once you are done, use !rfinish to save the changes.')
            def pred(m):
                return m.author == message.author and m.channel == message.channel
            while True:
                foundMessage = await client.wait_for('message', check=pred)
                if foundMessage.content.lower().startswith('!rfinish'):
                    with open('./{0}/{1}.txt'.format(message.guild.id, message.content[7:]), 'w+') as outfile:
                        json.dump(changingData, outfile, indent=4)
                        break
                elif foundMessage.content.lower().startswith('!rrole add'):
                    chosenEmote, chosenRole = foundMessage.content[11:].split('-')[0], foundMessage.content[11:].split('-')[1]
                    if chosenRole.lower() == 'none':
                        changingData[chosenEmote] = chosenNick
                        changingData['allReactions'].append(chosenEmote)
                        await messageObj.add_reaction(chosenEmote[2:-1])
                    else:
                        changingData['allReactions'].append(chosenEmote)
                        changingData['allRoles'].append(chosenRole)
                        changingData[chosenEmote] = chosenRole 
                        await messageObj.add_reaction(chosenEmote[2:-1])
                elif foundMessage.content.lower().startswith('!rrole remove'):
                    chosenEmote = foundMessage.content[14:]
                    del changingData['allRoles'][changingData['allRoles'].index(changingData[chosenEmote])]
                    del changingData['allReactions'][changingData['allReactions'].index(chosenEmote)]
                    del changingData[chosenEmote]
                    await messageObj.remove_reaction(chosenEmote[2:-1])
                elif foundMessage.content.lower().startswith('!rnick add'):
                    chosenEmote, chosenNick = foundMessage.content[11:].split('-')[0], foundMessage.content[11:].split('-')[1]
                    if chosenNick.lower() == 'none':
                        changingData['nameStuff'][chosenEmote] = chosenNick
                        changingData['nameStuff']['allReactions'].append(chosenEmote)
                        await messageObj.add_reaction(chosenEmote[2:-1])
                    else:
                        changingData['nameStuff'][chosenEmote] = chosenNick
                        changingData['nameStuff']['allReactions'].append(chosenEmote)
                        changingData['nameStuff']['allNames'].append(chosenNick) 
                elif foundMessage.content.lower().startswith('!rnick remove'):
                    chosenEmote = foundMessage.content[14:]
                    if changingData['nameStuff'][chosenEmote].lower() != 'none':
                        del changingData['nameStuff']['allNames'][changingData['nameStuff']['allNames'].index(changingData['nameStuff'][chosenEmote])]
                    del changingData['nameStuff']['allReactions'][changingData['nameStuff']['allReactions'].index(chosenEmote)]
                    del changingData['nameStuff'][chosenEmote]
                else:
                    await message.channel.send('Unexpected input, if you are trying to exit, please use !rfinish')
        if message.content.lower().startswith('!rhelp'):
            await message.channel.send("""
    Note: only custom emotes work currently, this is being worked on\n
    Please use the actual emote, and not just the name\n
    !rstart (Message ID), This will start the setup of a role assign\n
    !rfinish, This will complete the edit or the setup of a message.\n
    !rrole add (Emote)-(Role name, case sensitive), This will add emote detection for the selected message, only works during a setup or an edit\n
    !rrole remove (Emote), This will remove emote detection for the selected message, only works during an edit\n
    !rnick add (Emote)-(What to add to the end of the users name), This will add emote detection for the selected message, only works during a setup or an edit\n
    !rnick remove (Emote), This will remove emote delection for the selected message, only works during an edit\n
    Due to the way discord processes reactions, when removing a reaction from an already setup message, you will have to remove the user's reactions from that section.\n
    Replacing the nickname or role segment of any command with "none" will remove all the nicknames and roles from the user that the message wouldve given.  
    """)

        if message.content.lower().startswith('!ecreate'):
            pickedChannel = message.content[8:]
            try:
                channelObj = client.get_channel(int(pickedChannel))
            except:
                return
            await message.channel.send('Embed creation started, please use !etitle and !etext to determine the title and text for the embed')
            def pred(m):
                return m.author == message.author and m.channel == message.channel
            while True:
                foundMessage = await client.wait_for('message', check=pred)
                if foundMessage.content.lower().startswith('!etitle'):
                    eTitle = foundMessage.content[8:]
                elif foundMessage.content.lower().startswith('!etext'):
                    eDesc = foundMessage.content[7:]
                elif foundMessage.content.lower().startswith('!efinish'):
                    break
                else:
                    await message.channel.send('Unexpected input, please use !etitle and !etext to give the title and text for the embed')
            embed = discord.Embed(title=eTitle, description=eDesc)
            await channelObj.send(embed=embed)
    except Exception as ex:
        print(ex)
        pass

@client.event
async def on_raw_reaction_add(payload):
    try:
        print(str(payload.emoji))
        user, server, msg = client.get_guild(payload.guild_id).get_member(payload.user_id), client.get_guild(payload.guild_id), await client.get_channel(payload.channel_id).get_message(payload.message_id)
        print(str(user.display_name))
        with open('./{0}/{1}.txt'.format(payload.guild_id, payload.message_id), 'r') as jsonfile: ## Loads the JSOn file of the message
            data = json.load(jsonfile)
        if len(data['allRoles']) > 0:
            for role in data['allRoles']:
                if data[str(payload.emoji)] == 'none':
                    for role3 in user.roles:
                        if role3.name.lower() == role.lower():
                            await user.remove_roles(role3)
                    await msg.remove_reaction(str(payload.emoji)[2:-1], user)
                elif role != data[str(payload.emoji)]: ## Finds every role that isnt the picked one
                    while role.lower() in [y.name.lower() for y in user.roles]:
                        for role2 in server.roles:
                            if role2.name == role: ## Find the role object that needs to be removed, assigned to pickedRole
                                pickedRole = role2
                        await user.remove_roles(pickedRole)
                elif role == data[str(payload.emoji)]: ## Finds the role that is the picked one
                    while role.lower() not in [y.name.lower() for y in user.roles]:
                        for role2 in server.roles:
                            if role2.name == role: ## Find the role object that needs to be added, assigned to pickedRole
                                pickedRole = role2
                        await user.add_roles(pickedRole)
                for react in data['allReactions']:
                    if react != str(payload.emoji): ## Removes every reaction except from the chosen option
                        await msg.remove_reaction(react[2:-1], user)
        #for nickname in data['nameStuff']['allNames']:
        if data['nameStuff'][str(payload.emoji)] == 'none':
            tempNick = str(user.display_name)
            for name in data['nameStuff']['allNames']:
                tempNick = tempNick.replace(name, '')
            await user.edit(nick=tempNick)
            await msg.remove_reaction(str(payload.emoji)[2:-1], user)
        else: #nickname == data['nameStuff'][str(payload.emoji)]:
            await user.edit(nick=str(user.display_name) + data['nameStuff'][str(payload.emoji)])
        for react in data['nameStuff']['allReactions']:
            await msg.remove_reaction(react[2:-1], user)
    except Exception as ex:
        print(ex)

client.run(sys.argv[1])
