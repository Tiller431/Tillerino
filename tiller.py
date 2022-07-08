import discord
import os
import time
from dotenv import load_dotenv
from beatmaps import calc
from beatmaps import mods
from beatmaps import mods
from api import osu
from db import db
from beatmaps import ow
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
color = 0xff00e0
bot = discord.Client()


@bot.event
async def on_ready():
    print("initializing DB")
    db.initDB()
    print("DB initialized")
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
        msg += "!rs <username/userid> - Displays the user's recent score\n"
        await message.channel.send(msg)
        return
    
    if message.content.startswith(">rs"):
        try:
            userID = int(message.content.split(" ")[1])
        except:
            try:
                userID = osu.getUserID(message.content.split(" ")[1])
            except:
                userID = db.getUIDfromDID(message.author.id)
                if userID == None:
                    await message.channel.send("Please set your osu! username with !osuset <username> or do !r <username>")
                    return

            
        #user = db.getUser(userID)
        #if user is None:
            #await message.channel.send("User not found")
            #return
        recentScore = osu.getUserRecent(userID, 1)[0]
        if recentScore is None:
            await message.channel.send("{} has no recent score".format(osu.getUsername(userID)))
            return
        #db.getUserTop(userID, 1) example: {"beatmap_id":"987654","score":"1234567","maxcombo":"421","count50":"10","count100":"50","count300":"300","countmiss":"1","countkatu":"10","countgeki":"50","perfect":"0","enabled_mods":"76","user_id":"1","date":"2013-06-22 9:11:16","rank":"SH"}
        mapstats = osu.getBeatmap(recentScore["beatmap_id"])


        
        if recentScore is None:
            print(recentScore)
            await message.channel.send("User has no recent scores")
            return
        recent = recentScore
        
        #db.getBeatmap example: {"approved":"1","submit_date":"2013-05-15 11:32:26","approved_date":"2013-07-06 08:54:46","last_update":"2013-07-06 08:51:22","artist":"Luxion","beatmap_id":"252002","beatmapset_id":"93398","bpm":"196","creator":"RikiH_","creator_id":"686209","difficultyrating":"5.744717597961426","diff_aim":"2.7706098556518555","diff_speed":"2.9062750339508057","diff_size":"4","diff_overall":"8","diff_approach":"9","diff_drain":"7","hit_length":"114","source":"BMS","genre_id":"2","language_id":"5","title":"High-Priestess","total_length":"146","version":"Overkill","file_md5":"c8f08438204abfcdd1a748ebfae67421","mode":"0","tags":"kloyd flower roxas","favourite_count":"140","rating":"9.44779","playcount":"94637","passcount":"10599","count_normal":"388","count_slider":"222","count_spinner":"3","max_combo":"899","storyboard":"0","video":"0","download_unavailable":"0","audio_unavailable":"0"}

        
        recent["acc"] = calc.calcACC(int(recent["count300"]), int(recent["count100"]), int(recent["count50"]), int(recent["countmiss"]))
        recent["realmods"] = mods.readableMods(int(recent["enabled_mods"]))
        recent["notes_hit"] = int(recent["countmiss"]) + int(recent["count50"]) + int(recent["count100"]) + int(recent["count300"])
        recent["pp"] = calc.calcPlay(int(recent["beatmap_id"]), recent["realmods"], int(recent["notes_hit"]), int(recent["maxcombo"]), acc=recent["acc"], one=int(recent["count100"]), fif=int(recent["count50"]), misses=int(recent["countmiss"]))
        recent["pp_iffc"] = calc.calcPlay(int(recent["beatmap_id"]), recent["realmods"], 0, 0, acc=recent["acc"], one=int(recent["count100"]), fif=int(recent["count50"]), misses=0)


        desc = ""
        desc += "▸ {} ▸ {}PP ({}PP for {}% FC) ▸ {}%\n".format(recent["rank"], recent["pp"], recent["pp_iffc"], recent["acc"], recent["acc"])
        desc += "▸ {} ▸ x{}/{} ▸ [{}/{}/{}/{}]\n".format(recent["score"], recent["maxcombo"], mapstats["max_combo"], recent["count300"], recent["count100"], recent["count50"], recent["countmiss"])
        
        if recent["rank"] == "F":
            title = "{} [{}] +{} FAILED".format(mapstats["title"], mapstats["version"], recent["realmods"])
            desc += "▸ **Map Completion:** {}%".format(round((int(recent["notes_hit"]) / int(mapstats["max_combo"])) * 100, 2) )
        else:
            title = "{} [{}] +{}".format(mapstats["title"], mapstats["version"], recent["realmods"])
        
        embed = discord.Embed(description=desc, title=title, url="https://osu.ppy.sh/b/{}".format(recent["beatmap_id"]), colour=color)
        embed.set_thumbnail(url="https://b.ppy.sh/thumb/{}l.jpg".format(mapstats["beatmapset_id"]))
        embed.set_footer(text="score set at {}".format(recent["date"]))
        await message.channel.send("**{}'s Recent Score**".format(osu.getUsername(userID)), embed=embed)

        calc.calcAll(osu.getBeatmap(int(recentScore["beatmap_id"]))["beatmapset_id"])
        db.updateUser(userID)
        
        return

    if message.content.startswith("!osuset"):
        try:
            username = message.content.split(" ")[1]
        except:
            await message.channel.send("Please enter a valid username")
            return
        userID = osu.getUserID(username)
        if userID == None:
            await message.channel.send("Username not found")
            return
        if db.getUser(userID) is None:
            print(message.author.id)
            db.createUser(message.author.id, username)
        
        await message.channel.send("{} is now set to {}".format(message.author.mention, username))

    if message.content.startswith("!calcowlb"):
        try:
            beatmapID = message.content.split(" ")[1]
        except:
            await message.channel.send("Please enter a valid beatmap ID")
            return
        beatmap = osu.getBeatmap(beatmapID)
        if beatmap is None:
            await message.channel.send("Beatmap not found")
            return
        ow.calcOWFromLB(beatmapID)
        await message.channel.send("Calculated all players on {} leaderboard!".format(beatmap["title"]))

    if message.content.startswith("!r"):
        userid = db.getUIDfromDID(message.author.id)
        if userid is None:
            await message.channel.send("You are not registered. Please use !osuset <username> to register.")
            return

        #get random beatmap
        beatmap = db.getRandomOWmap(userid)
        if beatmap is None:
            await message.channel.send("Not enough maps in the database. \nPlease use !calcowlb <beatmapID> to calculate a leaderboard to load more maps into the DB.")
            return
        beatmap = osu.getBeatmap(beatmap)
        
        #create embed
        embed = discord.Embed(description="**{}**".format(beatmap["title"]), title="{} [{}]".format(beatmap["artist"], beatmap["version"]), url="https://osu.ppy.sh/b/{}".format(beatmap["beatmap_id"]), colour=color)
        embed.set_thumbnail(url="https://b.ppy.sh/thumb/{}l.jpg".format(beatmap["beatmapset_id"]))

        await message.channel.send("**{}'s Farm Map**".format(osu.getUsername(userid)), embed=embed)



    

bot.run(DISCORD_TOKEN)