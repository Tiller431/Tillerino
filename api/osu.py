from http.client import ResponseNotReady
from linecache import cache
import requests
import json
import os
from dotenv import load_dotenv
from logger import log
from beatmaps import mods as m

load_dotenv()
cachePath = "cache/osu/"
apiKey = os.getenv("OSU_API_KEY")

def getBeatmap(beatmapID):
    beatmapID = str(beatmapID)
    url = "https://osu.ppy.sh/api/get_beatmaps?k=" + apiKey + "&b=" + beatmapID
    log.api("Getting beatmap from osu!api with beatmapid: " + beatmapID)
    response = requests.get(url)
    response = response.json()[0]
    return response

def getUser(userID):
    userID = str(userID)
    url = "https://osu.ppy.sh/api/get_user?k=" + apiKey + "&u=" + userID
    log.api("Getting user from osu!api with userid: " + userID)
    response = requests.get(url)
    response = response.json()
    return response

def getUserTop(userID, limit):
    userID = str(userID)
    limit = str(limit)
    url = "https://osu.ppy.sh/api/get_user_best?k=" + apiKey + "&u=" + userID + "&limit=" + limit
    log.api("Getting user top plays from osu!api with userid: " + userID)
    response = requests.get(url)
    response = response.json()
    return response

def getUserRecent(userID, limit):
    userID = str(userID)
    limit = str(limit)
    url = "https://osu.ppy.sh/api/get_user_recent?k=" + apiKey + "&u=" + userID + "&limit=" + limit
    log.api("Getting user recent plays from osu!api with userid: " + userID)
    response = requests.get(url)
    response = response.json()
    try:
        if limit == "1":
            response = response[0]
            return response
        return response
    except IndexError:
        return None

def getOsu(beatmapID):
    #cache/osu/beatmapID.osu
    beatmapID = str(beatmapID)
    url = "https://osu.ppy.sh/osu/{}".format(beatmapID)
    log.api("Getting beatmap data for: " + beatmapID)
    response = requests.get(url)
    if os.path.exists(cachePath + beatmapID + ".osu"):
        os.remove(cachePath + beatmapID + ".osu")
    
    with open(cachePath + beatmapID + ".osu", "w") as f:
        f.write(response.text)
    return True

def getUserID(username):
    username = str(username)
    url = "https://osu.ppy.sh/api/get_user?k=" + apiKey + "&u=" + username
    log.api("Getting userid from osu!api with username: " + username)
    response = requests.get(url)
    response = response.json()
    try:
        return int(response[0]["user_id"])
    except IndexError:
        return None

def getUsername(userID):
    userID = str(userID)
    url = "https://osu.ppy.sh/api/get_user?k=" + apiKey + "&u=" + userID
    log.api("Getting username from osu!api with userid: " + userID)
    response = requests.get(url)
    response = response.json()
    return response[0]["username"]

def getAveragePPTOP(userID, limit):
    userID = str(userID)
    limit = str(limit)
    url = "https://osu.ppy.sh/api/get_user_best?k=" + apiKey + "&u=" + userID + "&limit=" + limit
    log.api("Getting average pp for top plays from osu!api with userid: " + userID)
    response = requests.get(url)
    response = response.json()
    pp = 0
    for i in response:
        pp += float(i["pp"])

    if pp == 0:
        return 0
    return pp / len(response)

def getBeatmapSet(beatmapSetID):
    beatmapSetID = str(beatmapSetID)
    url = "https://osu.ppy.sh/api/get_beatmaps?k=" + apiKey + "&s=" + beatmapSetID
    log.api("Getting beatmap set from osu!api with beatmapsetid: " + beatmapSetID)
    response = requests.get(url)
    response = response.json()
    return response

def getBeatmapSetID(beatmapID):
    beatmapID = str(beatmapID)
    url = "https://osu.ppy.sh/api/get_beatmaps?k=" + apiKey + "&b=" + beatmapID
    log.api("Getting beatmap set id from osu!api with beatmapid: " + beatmapID)
    response = requests.get(url)
    response = response.json()
    return response[0]["beatmapset_id"]

def getBeatmapLeaderboard(beatmapID, limit=50):
    beatmapID = str(beatmapID)
    limit = str(limit)
    url = "https://osu.ppy.sh/api/get_scores?k=" + apiKey + "&b=" + beatmapID + "&limit=" + limit
    log.api("Getting beatmap leaderboard from osu!api with beatmapid: " + beatmapID)
    response = requests.get(url)
    response = response.json()
    return response

def getScore(scoreID):
    scoreID = str(scoreID)
    url = "https://osu.ppy.sh/api/get_scores?k=" + apiKey + "&s=" + scoreID
    log.api("Getting score from osu!api with scoreid: " + scoreID)
    response = requests.get(url)
    response = response.json()
    return response

def getUserMods(userID):
    userID = str(userID)
    userScores = getUserTop(userID, 50)
    #get average used mods
    hd = 0.0001
    hr = 0.0001
    dt = 0.0001
    log.api("Getting average mods used by user from osu!api with userid: " + userID)
    for i in userScores:
        i["enabled_mods"] = int(i["enabled_mods"])
        if i["enabled_mods"] & m.mods.DOUBLETIME > 0:
            dt += 1

        if i["enabled_mods"] & m.mods.HARDROCK > 0:
            hr += 1

        if i["enabled_mods"] & m.mods.HIDDEN > 0:
            hd += 1

    if (dt / len(userScores) > 0.3) & (hd / len(userScores) > 0.3):
        log.debug("User uses double time and hidden")
        return m.mods.DOUBLETIME + m.mods.HIDDEN

    if (hr / len(userScores) > 0.3) & (hd / len(userScores) > 0.3):
        log.debug("User uses hardrock and hidden")
        return m.mods.HARDROCK + m.mods.HIDDEN

    if (dt / len(userScores) > 0.3):
        log.debug("User uses double time")
        return m.mods.DOUBLETIME

    if (hr / len(userScores) > 0.3):
        log.debug("User uses hardrock")
        return m.mods.HARDROCK

    if (hd / len(userScores) > 0.3):
        log.debug("User uses hidden")
        return m.mods.HIDDEN

    return m.mods.NOMOD

def doesUserTopExist(userID, beatmapID):
    userID = str(userID)
    limit = str(limit)
    url = "https://osu.ppy.sh/api/get_user_best?k=" + apiKey + "&u=" + userID + "&limit=1"
    log.api("Getting user top plays from osu!api with userid: " + userID)

