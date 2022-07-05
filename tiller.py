import discord
import os
import time
from dotenv import load_dotenv
from beatmaps import calc
from db import db
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

bot = discord.Client()

@bot.event
async def on_ready():
    print("initializing DB")
    db.initDB()
    print("DB initialized")
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------")
    print(f"{bot.user.name} has connected to Discord!")
    time.sleep(5)
    await bot.change_presence(activity=discord.Game(name="osu! | !help"))

@bot.event
async def on_message(message):

    if message.author == bot.user:
        return
	
    if message.content.startswith("!help"):
        msg = ""
        msg += "!help - Displays this message\n"
        msg += "!calc <beatmapid> - Calculates PP for the beatmap\n"
        await message.channel.send(msg)
        return

    if message.content.startswith("!calc"):
        try:
            beatmapID = int(message.content.split(" ")[1])
        except:
            await message.channel.send("Please enter a valid beatmap ID\nUsage: !calc <beatmapid>")
            return
        pp = calc.calcPP(beatmapID)
        await message.channel.send(pp)
        return
        
    

bot.run(DISCORD_TOKEN)