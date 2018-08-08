import discord, asyncio, math, sys
from discord.ext import commands

if not discord.opus.is_loaded():
    discord.opus.load_opus("opus")

class VoiceEntry:
    def __init__(self, message, player):
        self.requester = message.author
        self.channel = message.channel
        self.player = player

    def __str__(self):
        template = """
        ɴᴏᴡ ᴘʟᴀʏɪɴɢ: **{0.title}**
 ─────:white_circle:────────────────────── ◄◄⠀▐▐ ⠀►►⠀⠀　　⠀ **0:10** / **{1}**　　⠀ ───○ :loud_sound:⠀ᴴᴰ :gear:️ ❐ ⊏⊐
 """
        fmt = "{1.display_name} requested {0.title} by {0.uploader}"
        duration = self.player.duration
        if duration:
            duration2 = " {0[0]}:{0[1]}".format(divmod(duration, 60))
        return template.format(self.player, duration2).replace("@ m ", "")
        #return fmt.format(self.player, self.requester)

class VoiceState:
    def __init__(self, bot):
        self.current = None
        self.voice = None
        self.bot = bot
        self.playNextSong = asyncio.Event()
        self.songs = asyncio.Queue()
        self.skipVotes = set()
        self.audioPlayer = self.bot.loop.create_task(self.audioPlayerTask())
        self.songList = []

    def isPlaying(self):
        if self.voice == None or self.current == None:
            return False
        player = self.current.player
        return not player.is_done()
    
    @property
    def player(self):
        return self.current.player

    def skip(self):
        self.skipVotes.clear()
        if self.isPlaying():
            self.player.stop()

    def toggleNext(self):
        self.bot.loop.call_soon_threadsafe(self.playNextSong.set)
        del self.songList[0]

    async def audioPlayerTask(self):
        while True:
            self.playNextSong.clear()
            self.current = await self.songs.get()
            await self.bot.send_message(self.current.channel, str(self.current))
            self.current.player.start()
            await self.playNextSong.wait()
class Music:
    def __init__(self, bot):
        self.bot = bot
        self.voiceStates = {}

    def getVoiceState(self, server):
        state = self.voiceStates.get(server.id)
        if state == None:
            state = VoiceState(self.bot)
            self.voiceStates[server.id] = state

        return state
    
    def ___unload(self):
        for state in self.voiceStates.values():
            try:
                state.audioPlayer.cancel()
                if state.voice:
                    self.bot.create_task(state.voice.disconnect())
            except:
                pass

    @commands.command(pass_context=True, no_pm=True)
    async def summon(self, ctx):
        """Summons the bot to join your voice channel."""
        summoned_channel = ctx.message.author.voice_channel
        if summoned_channel is None:
            await self.bot.say('You are not in a voice channel.')
            return False

        state = self.getVoiceState(ctx.message.server)
        if state.voice is None:
            state.voice = await self.bot.join_voice_channel(summoned_channel)
        else:
            await state.voice.move_to(summoned_channel)

        return True

    @commands.command(pass_context=True)
    async def play(self, ctx, *, song : str):
        if ctx.message.channel.name != "voice":
            await self.bot.say("This channel does not allow music commands due to the spam it causes, please switch to #voice")
            return
        summoned_channel = ctx.message.author.voice_channel
        if summoned_channel is None:
            await self.bot.say('You are not in a voice channel.')
            return False

        state = self.getVoiceState(ctx.message.server)
        if state.voice is None:
            state.voice = await self.bot.join_voice_channel(summoned_channel)
        else:
            await state.voice.move_to(summoned_channel)
        state = self.getVoiceState(ctx.message.server)
        opts = {
            'default_search': 'auto',
            'quiet': True,
        }
        
        try:
            player = await state.voice.create_ytdl_player(song + "nightcore", ytdl_options = opts, after = state.toggleNext)
            if player.duration >= 3600:
                raise SyntaxError
        except Exception as ex:
            fmt = "Something went wrong, either the song cannot be found or the song is longer than one hour."
            await self.bot.send_message(ctx.message.channel, fmt)
            print(ex)
        else:
            entry = VoiceEntry(ctx.message, player)
            await self.bot.say("{0} has been queued by {1}".format(entry.player.title, ctx.message.author.display_name).replace("@", ""))
            await state.songs.put(entry)
            state.songList.append(entry.player.title + ctx.message.author.display_name)

    @commands.command(pass_context=True, no_pm=True)
    async def skip(self, ctx):
        state = self.getVoiceState(ctx.message.server)
        if not state.isPlaying():
            await self.bot.say('Not playing any music right now...')
            return

        voter = ctx.message.author
        if voter == state.current.requester:
            await self.bot.say('The user who requested this song has skipped it')
            state.skip()
        elif voter.id not in state.skipVotes:
            state.skipVotes.add(voter.id)
            total_votes = len(state.skipVotes)
            voteCap = math.ceil(int(len(state.current.channel.voice_members) - 1) / 2)
            if total_votes >= voteCap:
                await self.bot.say('Vote goal reached, skipping song.')
                state.skip()
            else:
                await self.bot.say('Skip vote added. Progress: [{0}/{1}]'.format(total_votes, voteCap).replace("@", ""))
        else:
            await self.bot.say('You cannot contribute to the skip goal because you have already voted.')

    @commands.command(pass_context=True)
    async def stop(self, ctx):
        if not (ctx.message.channel.permissions_for(ctx.message.author).manage_messages or ctx.message.author.id == "261926271892717569"):
            return
        server = ctx.message.server
        state = self.getVoiceState(server)
        if state.isPlaying():
            player = state.player
            player.stop()

        try:
            state.audioPlayer.cancel()
            del self.voiceStates[server.id]
            await state.voice.disconnect()
        except Exception as ex:
            print(ex)
            pass
    
    @commands.command(pass_context=True)
    async def priorityskip(self, ctx):
        if not (ctx.message.channel.permissions_for(ctx.message.author).manage_messages or ctx.message.author.id == "261926271892717569"):
            return
        server = ctx.message.server
        state = self.getVoiceState(server)
        await self.bot.say('A priority skip as been used on this song, skipping.')
        state.skip()       
    @commands.command(pass_context=True)
    async def volume(self, ctx, *, vol : int):
        state = self.getVoiceState(ctx.message.server)
        if ctx.message.author == state.current.requester and vol > 0 and vol < 101 and state.isPlaying:
            state.player.volume = vol / 100
            await self.bot.say("Set the volume to {0}".format(state.player.volume))
    @commands.command(pass_context=True)
    async def queue(self, ctx):
        state = self.getVoiceState(ctx.message.server)
        copyQueue = state.songs
        print(state.songList)
bot = commands.Bot(command_prefix=commands.when_mentioned_or('alexa '), description='alexa play despacito')
bot.add_cog(Music(bot))
@bot.event
async def on_ready():
    print('Logged in as:\n{0} (ID: {0.id})'.format(bot.user))
bot.run(sys.argv[1])
