from db import db
from api import osu


def calcOwTPs(userid, limit=5):
    userPlays = osu.getUserTop(userid, limit=limit)
    ow = 0
    for play in userPlays:
        beatmapid = play["beatmap_id"]
        mods = play["enabled_mods"]
        if db.isMapInDB(beatmapid, mods):
            continue
        #save score to db
        if db.isScoreOW(play["score_id"]):
            #skip if already in db
            continue
        db.saveScore(beatmapid, play["user_id"], play["score_id"], play["enabled_mods"], play["pp"], ow)
        if not db.isMapOW(beatmapid):
            db.saveOWmap(beatmapid)
        db.updateOWscore(play["beatmap_id"])
        ow += 1

def calcOWFromLB(beatmapid):
    scores = osu.getBeatmapLeaderboard(beatmapid, limit=50)
    for score in scores:
        calcOwTPs(score["user_id"])



