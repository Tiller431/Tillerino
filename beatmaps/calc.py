import os
import json
from api import osu
from db import db
from logger import log

oppaiPath = "oppai"
cachePath = "cache/osu/"
calcMods = []
calcMods.append("NOMOD")
calcMods.append("HD")
calcMods.append("DT")
calcMods.append("HR")
calcMods.append("HDHR")
calcMods.append("HDDT")

calcAcc = []
calcAcc.append("90")
calcAcc.append("95")
calcAcc.append("96")
calcAcc.append("97")
calcAcc.append("98")
calcAcc.append("99")
calcAcc.append("99.5")
calcAcc.append("100")




def calcPP(beatmapid):
    beatmapid = str(beatmapid)
    osu.getOsu(beatmapid)
    ret = ""
    #oppai pathtoosu -ojson acc% +mods
    for mods in calcMods:
        final = []
        final.append(mods)
        if db.isMapInDB(beatmapid, mods):
            continue
        for acc in calcAcc:
            if mods != "NOMOD":
                #run "oppai pathtoosu -ojson acc%" and get the json
                log.debug("Calculating PP for {} with {}% accuracy and {} mods".format(beatmapid, acc, mods))
                output = os.popen("oppai " + cachePath + beatmapid + ".osu" + " -ojson " + acc + "% " + "+" + mods).read()
            else:
                log.debug("Calculating PP for {} with {}% accuracy and no mods".format(beatmapid, acc))
                output = os.popen("oppai " + cachePath + beatmapid + ".osu" + " -ojson " + acc + "%").read()

            #parse the json
            output = json.loads(output)
            #get the pp
            pp = round(output["pp"], 2)
            #print the pp
            print(beatmapid + " " + acc + "% +" + mods + ": " + str(pp))
            final.append(pp)
        #save the pp to the database
        formatted = "+**{}**: **90%**:{} **95%**:{} **96%**:{} **97%**:{} **98%**:{} **99%**:{} **99.5%**:{} **100%**:{}\n".format(mods, final[1], final[2], final[3], final[4], final[5], final[6], final[7], final[8])
        ret += formatted
        db.saveBeatmapData(beatmapid, round(output["stars"], 4), mods, final[1], final[2], final[3], final[4], final[5], final[6], final[7], final[8])
    return ret


def calcUserTop(userid, limit=25):
    userPlays = osu.getUserTop(userid, limit=limit)
    if userPlays is None:
        return None
    
    log.debug("Calculating top plays  for {}".format(userid))

    for play in userPlays:
        # example: {"beatmap_id":"987654","score":"1234567","maxcombo":"421","count50":"10","count100":"50","count300":"300","countmiss":"1","countkatu":"10","countgeki":"50","perfect":"0","enabled_mods":"76","user_id":"1","date":"2013-06-22 9:11:16","rank":"SH"}
        beatmapid = play["beatmap_id"]
        calcPP(beatmapid)

def calcACC(num300, num100, num50, nummiss):
    log.debug("Calculating accuracy for {} 300s, {} 100s, {} 50s, {} misses".format(num300, num100, num50, nummiss))
    prec = ((num300 * 300) + (num100 * 100) + (num50 * 50)) / ((num300 + num100 + num50 + nummiss) * 300)
    prec = prec * 100
    return round(prec, 2)

def calcPlay(mapID, mods, end=0, combo=0, acc=100, one=0, fif=0, misses=0):
    cmd = "{} {}{}.osu -ojson".format(oppaiPath, cachePath, mapID)
    osu.getOsu(mapID)
    if osu.getBeatmap(mapID) is False:
        return 0
    if mods != "nomod":
        cmd += " +{}".format(mods)
    cmd += " {}%".format(acc)
    if one > 0:
        cmd += " {}x100".format(one)
    if fif > 0:
        cmd += " {}x50".format(fif)  
    if misses > 0:
        cmd += " {}m".format(misses)
    if end > 0:
        cmd += " -end{}".format(end)
    if combo > 0:
        cmd += " {}x".format(combo)
    log.debug("Calculating PP for {} with {}% accuracy and {} mods".format(mapID, acc, mods))
    output = json.loads(os.popen(cmd).read())
    return int(output["pp"])

def calcAll(beatmapsetid):
    beatmaps = osu.getBeatmapSet(beatmapsetid)
    log.debug("Calculating PP for all maps in beatmapset: {}".format(beatmapsetid))
    for beatmap in beatmaps:
        calcPP(beatmap["beatmap_id"])
