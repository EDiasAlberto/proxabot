import discord, random, time, praw, os, asyncio, pyrebase, requests, youtube_dl
from discord import FFmpegPCMAudio, PCMVolumeTransformer
from discord.ext import commands, tasks
from dotenv import load_dotenv

coinIsDrop = False
numCoins = 0

#This loads in some secret variables for the connections to discord API and Firebase API
load_dotenv()
TOKEN=os.getenv("DISCORD_TOKEN")
EMAIL=os.getenv("EMAIL_FIREBASE")
PWORD_FIREBASE=os.getenv("PWORD_FIREBASE")
GOOGLE_APPLICATION_CREDS=os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

config = {
    "apiKey": "AIzaSyDtPkzN9bayRlhOEUpkz0e68bFITjU4Dsw",
    "authDomain": "proxabot-data.firebaseapp.com",
    "databaseURL": "https://proxabot-data.firebaseio.com",
    "projectId": "proxabot-data",
    "storageBucket": "proxabot-data.appspot.com",
    "messagingSenderId": "307753301122",
    "appId": "1:307753301122:web:5d9b4a4eef3faa42d1309b",
    "measurementId": "G-BZQ4PP7W6W",
    "serviceAccount": GOOGLE_APPLICATION_CREDS
}

#This initialises the bot with the prefix "$"
client=commands.Bot(command_prefix="$")

#This allows me to write my own help command.
client.remove_command("help")

async def coinDrop(message):
    global coinIsDrop
    global numCoins
    numCoins = random.randint(0, 1000)
    await message.channel.send(f"**EVENT**")
    await message.channel.send(f"Quick! Send \"claim\" to claim the coins!!")
    await message.channel.send("You have 30 seconds!")
    coinIsDrop = True
    await asyncio.sleep(30)
    coinIsDrop = False
    

#This is just a short event that runs when the bot connects. It will print out "Bot is ready", for when I'm debugging, and also set its status to "$help"
#It also loads all the functions of the bot from the other files.
@client.event
async def on_ready():
    for file in os.listdir("./cogs"):
        try:
            if file.endswith(".py"):
                client.unload_extension(f"cogs.{file[0:-3]}")
                client.load_extension(f"cogs.{file[0:-3]}")
        except commands.errors.ExtensionNotLoaded:
            client.load_extension(f"cogs.{file[0:-3]}")

    print("Bot is ready")
    await client.change_presence(activity = discord.Game("$help"))


#This is a simple "no u" response function because my sense of comedy as well as my sense of self is slowly deteriorating, please send help.
#I'm just kidding of course.
@client.event
async def on_message(message):

    found = False
    logData=[]
    responses1=["Still you","https://www.youtube.com/watch?v=TyfNZs2dPto",
                "ur dad", "It's not me, it's youuuuu.", "no u.", "uno reverse",
                "ur face", "undoubtedly u" ]
    if ("no u " in str(message.content.lower()) and not(message.author == client.user)) or (str(message.content.lower())=="no u"):
        reply=random.choice(responses1)
        await message.channel.send(reply)
    #elif "thank" in str(message.content.lower()) and not(message.author == client.user):
        #reply=random.choice(responses2)
        #await message.channel.send(reply)
    #if random.randint(0, 10)==7:
    #    await message.channel.send("Pokemon Spawned")
    #if message.author.id==284738961631608832 and random.randint(1, 100)>65:
        # await message.channel.send(message.content)

        



    await client.process_commands(message)



#This is a very messy and unorganised implementation of the help command.
#Actually... lemme shift all of this dictionary into a separate file.
#That's better.
@client.command()
async def help(ctx):
    author=ctx.message.author
    embed= discord.Embed( colour = discord.Colour.blue())
    embed.set_author(name="Help")

    with open("botData/commands.txt", "r") as file:
        for line in file:
            command, helpText = line.strip(",\n").replace("\"", "").split(":")
            embed.add_field(name=f"${command}", value=helpText, inline=False)
    
    await ctx.send(author, embed=embed)

#Always be plugging.
@client.command()
async def github(ctx):
    await ctx.send("https://github.com/EDiasAlberto/proxabot")
    

client.run(TOKEN)
