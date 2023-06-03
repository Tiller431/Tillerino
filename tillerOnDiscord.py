from dotenv import load_dotenv
from beatmaps import calc
from beatmaps import mods as m
from math import acos
from api import osu
from db import db
from db import settings as set
from beatmaps import ow
from logger import log
from beatmaps import maptypes as mt
import threading
import discord
import os
import time
load_dotenv()
WYSI = []
WYSI.append("727")
WYSI.append("7.27")
WYSI.append("72.7")
WYSI.append("7:27")


DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
color = 0xff00e0
bot = discord.Client()
botStatus = "osu! | V0.9.1"

@bot.event
async def on_ready():
    print(calc.calcPP(2137200, m.modsToEnum("HD")))
    log.debug("Initilizing DB")
    db.initDB()

    log.info(f"{bot.user.name} has connected to Discord!")
    time.sleep(5)
    log.info("Changing status to 'Playing {}'".format(botStatus))
    await bot.change_presence(activity=discord.Game(name=botStatus))

@bot.event
async def on_message_edit(message1, message2):
    #WYSI checker
    #get text from embed
    for wysi in WYSI:
        try:
            embed = str(message2.embeds[0].to_dict())
        except:
            continue
        if wysi in embed:
            await message2.channel.send("https://c.tenor.com/QqSkd-o9L8sAAAAS/aireu-wysi.gif")
            return
    for wysi in WYSI:
        if wysi in message2.content:
            await message2.channel.send("https://c.tenor.com/QqSkd-o9L8sAAAAS/aireu-wysi.gif")
            return

@bot.event
async def on_message(message):
    
    #WYSI checker
    #get text from embed
    for wysi in WYSI:
        try:
            embed = str(message.embeds[0].to_dict())
        except:
            continue
        if wysi in embed:
            await message.channel.send("https://c.tenor.com/QqSkd-o9L8sAAAAS/aireu-wysi.gif")
            return
    for wysi in WYSI:
        if wysi in message.content:
            await message.channel.send("https://c.tenor.com/QqSkd-o9L8sAAAAS/aireu-wysi.gif")
            return

    if message.author == bot.user:
        return
	
    if message.content.startswith("!help"):
        log.info("{} sent !help".format(message.author))
        msg = ""
        msg += "!help - Displays this message\n"
        msg += "!calc <beatmapid> - Calculates PP for the beatmap\n"
        msg += "!rs <username/userid> - Displays the user's recent score\n"
        await message.channel.send(msg)
        return        
    
    if message.content.startswith("!rs"):
        log.info("{} sent !rs".format(message.author))
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
        recentScore = osu.getUserRecent(userID, 1)
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
        recent["realmods"] = m.readableMods(int(recent["enabled_mods"]))
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
        log.debug("Sending recent score embed")
        await message.channel.send("**{}'s Recent Score**".format(osu.getUsername(userID)), embed=embed)

        #calc.calcAll(osu.getBeatmap(int(recentScore["beatmap_id"]))["beatmapset_id"])
        db.updateUser(userID)
        
        return

    if message.content.lower().startswith(">rs"):
        log.info("{} sent >rs. Not sending anything but calculating all top plays for all players on the LB".format(message.author))
        try:
            userID = int(message.content.split(" ")[1])
        except:
            try:
                userID = osu.getUserID(message.content.split(" ")[1])
            except:
                userID = db.getUIDfromDID(message.author.id)
                if userID == None:
                    await message.channel.send("Please set your osu! username with !osuset <username> to help find maps for future recommendations")
                    

            
        #user = db.getUser(userID)
        #if user is None:
            #await message.channel.send("User not found")
            #return
        recentScore = osu.getUserRecent(userID, 1)
        if recentScore is None:
            return
            
        #db.getUserTop(userID, 1) example: {"beatmap_id":"987654","score":"1234567","maxcombo":"421","count50":"10","count100":"50","count300":"300","countmiss":"1","countkatu":"10","countgeki":"50","perfect":"0","enabled_mods":"76","user_id":"1","date":"2013-06-22 9:11:16","rank":"SH"}
        mapstats = osu.getBeatmap(recentScore["beatmap_id"])


        
        if recentScore is None:
            print(recentScore)
            await message.channel.send("User has no recent scores")
            
        recent = recentScore
        #calcOwFromLB thread
        thread = threading.Thread(target=ow.calcOWFromLB, args=(mapstats["beatmap_id"],)).start()

        db.updateUser(userID)
        log.debug("Done calculating all top plays for all players on the LB")
        


    if message.content.startswith("!osuset"):
        try:
            username = message.content.split(" ")[1]
        except:
            await message.channel.send("Please enter a valid username")
            return
        log.info("{} sent !osuset. Setting their osu! username to {}".format(message.author, message.content.split(" ")[1]))
        userID = osu.getUserID(username)
        if userID == None:
            log.debug("'{}' osu! username is invalid".format(username))
            await message.channel.send("Username not found")
            return
        if db.getUser(message.author.id) is None:
            db.createUser(message.author.id, username)
        else:
            db.changeUsername(message.author.id, username)
        db.updateUser(userID)
        
        await message.channel.send("{} is now set to {}".format(message.author.mention, username))

    if message.content.startswith("!calcowlb"):
        log.info("{} sent !calcowlb. Calculating OW for all players on the LB".format(message.author))
        try:
            beatmapID = message.content.split(" ")[1]
        except:
            await message.channel.send("Please enter a valid beatmap ID")
            return
        beatmap = osu.getBeatmap(beatmapID)
        if beatmap is None:
            await message.channel.send("Beatmap not found")
            return
        thread = threading.Thread(target=ow.calcOWFromLB, args=(beatmapID,))
        thread.start()
        await message.channel.send("Calculated all players on {} leaderboard!".format(beatmap["title"]))

    if message.content.startswith("!r"):
        speed = False
        aim = False
        usermods = None
        log.info("{} sent !r. Getting an overweighted map.".format(message.author))
        userid = db.getUIDfromDID(message.author.id)
        if userid is None:
            await message.channel.send("You are not registered. Please use !osuset <username> to register.")
            return

        if len(message.content) > 3:
            #get mods and type
            try:
                types = message.content.split(" ")[1]
                if types == "speed":
                    speed = True
                elif types == "aim":
                    aim = True
                else:
                    await message.channel.send("Please enter a valid type !r (speed/aim) (mods)")
                    return
                
                usermods = m.modsToEnum(message.content.split(" ")[2])

            except:
                pass

        
        beatmapID, mods, numOfBM = db.getRandomOWmap(userid, mods=usermods)
        #print(beatmapID, mods, numOfBM)

        if speed and aim:
            await message.channel.send("Please only choose one mod type: speed or aim")
            return
        
        if speed:
            if beatmapID is None:
                log.error("No maps found for user {}".format(userid))
                await message.channel.send("Not enough maps in the database. \nPlease use !calcowlb <beatmapID> to calculate a leaderboard to load more maps into the DB.")
                return
            while mt.isSpeed(beatmapID) == False:
                beatmapID, mods, numOfBM = db.getRandomOWmap(userid, mods=usermods)
                print(beatmapID, mods, numOfBM)
        elif aim:
            if beatmapID is None:
                log.error("No maps found for user {}".format(userid))
                await message.channel.send("Not enough maps in the database. \nPlease use !calcowlb <beatmapID> to calculate a leaderboard to load more maps into the DB.")
                return
            while mt.isAim(beatmapID) == False:
                beatmapID, mods, numOfBM = db.getRandomOWmap(userid, mods=usermods)
                print(beatmapID, mods, numOfBM)
        
        beatmap = osu.getBeatmap(beatmapID)
        ppjson = calc.calcPP(beatmapID, mods)
        #create embed
        description = ""
        description += "▸ {}★ ▸ {} bpm ▸ {} ▸ +{}\n".format(round(float(beatmap["difficultyrating"]), 2), round(float(beatmap["bpm"]) * 1.5) if mods & m.mods.DOUBLETIME > 0 else beatmap["bpm"], time.strftime("%M:%S", time.gmtime(int(beatmap["hit_length"]))), m.readableMods(int(mods)))
        #calc pp
        ppStats = db.getPP(beatmap["beatmap_id"], mods)
        #add pp stats (95% FC, 98% FC, 100% FC)
        #ppstats = ppStats[1], ppStats[4], ppStats[7]
        log.debug("ppstats: {}".format(ppStats))
        description += "▸ 95% > {}pp ▸ 98% > {}pp ▸ 100% > {}pp\n".format(round(float(ppStats[1]), 2), round(float(ppStats[4]), 2), round(float(ppStats[7]), 2))
        description += "AimPP: {}pp ▸ SpeedPP: {}pp ▸ AccPP: {}pp".format(round(ppjson["aim_pp"], 2), round(ppjson["speed_pp"], 2), round(ppjson["acc_pp"], 2))

        embed = discord.Embed(description=description, title="{} - {} [{}]".format(beatmap["artist"], beatmap["title"], beatmap["version"]), url="https://osu.ppy.sh/b/{}".format(beatmap["beatmap_id"]), colour=color)
        embed.set_thumbnail(url="https://b.ppy.sh/thumb/{}l.jpg".format(beatmap["beatmapset_id"]))
        log.debug("Sending random farm map embed and osu!direct link")
        threading.Thread(target=ow.calcOWFromLB, args=(beatmap["beatmap_id"],)).start()
        await message.channel.send("**{}'s Farm Map**\nosu!direct link: <osu://b/{}>".format(osu.getUsername(userid), beatmap["beatmap_id"]), embed=embed)
        return

    if message.content.startswith("!settings"):
        try:
            setting = message.content.split(" ")[1]
            value = message.content.split(" ")[2]
        except:
            await message.channel.send('Please enter a valid setting and value. Example: !settings maptype speed\nAvailable settings:\n"preferedmods" - Automatic prefered mods not the right mods? Example: HDHR\n"maptype" - Do you prefer aim maps over stream maps? (speed, aim)\nMore settings coming soon! (Have some ideas? Msg Tiller)')
            return

        if setting == "preferedmods":
            log.info("{} sent !settings preferedmods. Setting prefered mods to {}".format(message.author, value))
            set.setSettings(message.author.id, "preferedmods", value)
            await message.channel.send("Prefered mods set to {}".format(value))

        if setting == "maptype":
            log.info("{} sent !settings maptype. Setting maptype to {}".format(message.author, value))
            set.setSettings(message.author.id, "maptype", value)
            await message.channel.send("Maptype set to {}".format(value))


        
        
        



    

bot.run(DISCORD_TOKEN)