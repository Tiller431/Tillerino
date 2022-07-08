from db import db
from api import osu
from beatmaps import ow
from beatmaps import mods
from logger import log

def recalculateOW(beatmapid):
    scores = db.getAllScores()
    #for score in scores:
