import discord, random, time, praw, os, youtube_dl
from discord import FFmpegPCMAudio, PCMVolumeTransformer
from discord.ext import commands
from dotenv import load_dotenv

class Voice(commands.Cog):

    def __init__(self, client):
        self.client = client

    #This command allows my bot to join voice channels.
    #Initially, I was planning to develop this, but then I just decided to use it to cope with loneliness.
    #Changed my mind and now it plays a random song from the folder audioFiles
    #Changed my mind again and just removed that function because it takes up a lot of space on
    @commands.command()
    async def join(self, ctx):
        global voice 

        channel = ctx.author.voice.channel
        voice = await channel.connect()
        await ctx.send("I have joined the voice chat.")

    #This uses the youtube_dl library to download a video from youtube and play the 
    @commands.command()
    async def play(self, ctx, url, volume=0.5):
        global voice
        try:
            os.remove("song.wav")
        except PermissionError:
            await ctx.send("There is currently a song playing, please wait.")
            return
        except Exception as e:
            print(e)
            pass
        ydlOpts  = {'format': 'bestaudio/best',
                     'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
                     'restrictfilenames': True,
                     'noplaylist': True,
                     'nocheckcertificate': True,
                     'ignoreerrors': False,
                     'logtostderr': False,
                     'quiet': True,
                     'no_warnings': True,
                     'default_search': 'auto',
                     'source_address': '0.0.0.0',
                     'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'wav',
                        'preferredquality': '192', }]
                    }

        channel = ctx.author.voice.channel
        if ctx.voice_client is None:    
            voice = await channel.connect()
        with youtube_dl.YoutubeDL(ydlOpts) as ydl:
            ydl.download([url])

        for file in os.listdir("./"):
            if file.endswith(".wav"):
                os.rename(file, "song.wav")
        
        chosenSong = FFmpegPCMAudio("song.wav")
        voice.play(chosenSong)
        voice.source = PCMVolumeTransformer(voice.source)
        voice.source.volume= volume



    #This is for trolling ProxaBot
    @commands.command()
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()



def setup(client):
    for command in commands.Cog.get_commands(Voice):
        client.remove_command(command.name)
    client.add_cog(Voice(client))