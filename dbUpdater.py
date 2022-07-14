from db import db
from beatmaps import calc
from beatmaps import ow
from beatmaps import mods
from api import osu
from logger import log
import threading

def thread(scores):
    for score in scores:
        #get stats
        beatmapid = score[0]
        beatmapsetid = score[1]
        userid = score[2]
        scoreid = score[3]
        mods = score[4]
        pp = score[5]
        owRank = score[6]

        #update ow beatmap
        if not db.isMapOW(beatmapid, mods):
            db.saveOWmap(beatmapid, mods)
        db.updateOWscore(beatmapid, mods)

        


#get all scores in db
scores = db.getAllScores()
log.debug("# of scores: {}".format(len(scores)))

#thread scores
threads = []

#4 threads
for i in range(8):
    t = threading.Thread(target=thread, args=(scores[i::8],))
    threads.append(t)
    t.start()


