from beatmaps import calc
from logger import log
def isAim(beatmapid):
    stats = calc.calcPP(beatmapid, 0)
    speed_pp = stats["speed_pp"]
    aim_pp = stats["aim_pp"]
    if aim_pp / speed_pp > 1:
        return True
    else:
        return False

def isSpeed(beatmapid):
    stats = calc.calcPP(beatmapid, 0)
    speed_pp = stats["speed_pp"]
    aim_pp = stats["aim_pp"]

    log.error("Speed: {} Aim: {} = {}".format(speed_pp, aim_pp, speed_pp / aim_pp))
    if speed_pp / aim_pp > 0.6:
        return True
    else:
        return False