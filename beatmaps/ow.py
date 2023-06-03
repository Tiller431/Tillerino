from db import db
from api import osu
from logger import log
import threading
import time


def calcOwTPs(userid, limit=30):
    userPlays = osu.getUserTop(userid, limit=limit)
    ow = 0
    for play in userPlays:
        beatmapid = play["beatmap_id"]
        mods = play["enabled_mods"]
        #if db.isMapInDB(beatmapid, mods):
            #continue
        #save score to db
        if db.isScoreOW(play["score_id"]):
            log.debug("already calculated user... skipping")
            break
        db.saveScore(beatmapid, play["user_id"], play["score_id"], play["enabled_mods"], play["pp"], ow)
        if not db.isMapOW(beatmapid, mods):
            db.saveOWmap(beatmapid, mods)
        db.updateOWscore(play["beatmap_id"], play["enabled_mods"])
        ow += 1

def calcOWFromLB(beatmapid):
    difficulties = osu.getBeatmapSet(osu.getBeatmapSetID(beatmapid))
    log.debug("Calculating OW for {}".format(beatmapid))
    numOfCalcs = len(difficulties) * 50 * 30
    timeMin = numOfCalcs / 20 / 60
    log.info("Calculating {} scores. Should take {} min or less!".format(numOfCalcs, timeMin))
    threads = []
    for dif in difficulties:
        scores = osu.getBeatmapLeaderboard(dif["beatmap_id"], limit=50)
        # 20 scores per thread
        if db.isScoreOW(scores[0]["score_id"]):
            log.debug("already calculated map... skipping")
            return
        for i in range(0, len(scores), 20):
            thread = threading.Thread(target=calcOwTPs, args=(scores[i]["user_id"],))
            thread.start()
            threads.append(thread)


    for thread in threads:
        thread.join()
    log.info("Done calculating {} scores".format(numOfCalcs))




