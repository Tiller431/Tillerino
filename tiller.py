import discord
import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

bot = discord.Client()

@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")

@bot.event
async def on_message(message):

    if message.author == bot.user:
        return
	
    if message.content.startswith("!help"):
        msg = ""
        msg += "!help - Displays this message\n"
        msg += "!calc <beatmapid> - Calculates PP for the beatmap\n"
        
    

bot.run(DISCORD_TOKEN)