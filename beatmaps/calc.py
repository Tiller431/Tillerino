import os
import json
from api import osu
from db import db
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
        for acc in calcAcc:
            if mods != "NOMOD":
                #run "oppai pathtoosu -ojson acc%" and get the json
                output = os.popen("oppai " + cachePath + beatmapid + ".osu" + " -ojson " + acc + "% " + "+" + mods).read()
            else:
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
        db.saveBeatmapData(beatmapid, mods, final[1], final[2], final[3], final[4], final[5], final[6], final[7], final[8])
    return ret



