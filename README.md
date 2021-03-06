# Welcome to the homepage of the OmniJeff Discord bot

You can use [this link](https://discordapp.com/api/oauth2/authorize?client_id=419504879426600971&permissions=0&scope=bot) to add the bot to your discord server.

OmniJeff is a Discord bot written in Python using the Discord.py API wrapper, with different modules of the bot running in different versions of the Discord.py wrapper.

## Features

### Dynamic Role Assign

Using the power of dynamic functions, OmniJeff can setup reaction-based role and nametag assigning in a few simple and secure commands. Only permitted users with the permissions to manage roles can create role assign, so you dont have to worry about rogue members creating a button to give admin privelages. Additionally, only the user who setup the role assign can edit the configuration. 

```markdown
!rstart *ID of the message to setup the reactions*
```
The !rstart command initialises the setup procedure and checks the creator of the message to see if their permissions are enough to permit the creation of a role assign. This also starts the creation session, and allows the other commands to be used.

```markdown
!rrole add *Custom Emote*-*Role name*
```
This pairs the emote and the role that it will assign. The command only accepts custom emotes and, if the user has nitro, can use emotes from other servers if OmniJeff is also in that same server. If the role name given is "None", the bot wil strip the reactor of all the roles that the other reactions would've provided. Please note that the emote has to be an actual usage of the emote, and not just the name. Role name is case sensitive.

```markdown
!rnick add *Custom Emote*-*String to append*
```
This pairs the emote and the string that it will append onto the reactors name. The command only accepts custom emotes and, if the user has nitro, can use emotes from other servers if OmniJeff is also in that same server. If the string given is "None", the bot wil strip the reactor of all the strings that the other reactions would've provided. Please note that the emote has to be an actual usage of the emote, and not just the name.

```markdown
!rfinish
```
This finishes the role assign creation process and saves the configuration file. Please note that the role assign will not function until the configuration has been saved.

```markdown
!redit *ID of the message the role assign is configurated on*
```
This starts the configuration editing session and the user is able to edit the configuration for the role assign. Only the user who created the initial role assign for the message will be able to change its settings. Some additional commands such as !rrole remove and !rnick remove will become enabled, wheras they were disabled during the initial setup period.

```markdown
!rrole remove *Custom Emote*
```
This removes the selected emote from the role assign configuration. This command is only avalible in the editing process and is disabled during the initial setup period.

```markdown
!rnick remove *Custom Emote*
```
This removes the selected emote from the role assign configuration. This command is only avalible in the editing process and is disabled during the initial setup period.

### Emote Analysis

From the second the OmniJeff bot is added to your server, it has begun creating a database of all the server emotes and has started counting everytime each individual one is used. This creates an emote profile for your individual server with data that can be used and analysed to produce graphs based on total emote usage.
