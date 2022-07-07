from linecache import cache
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
cachePath = "cache/osu/"
apiKey = os.getenv("OSU_API_KEY")

def getBeatmap(beatmapID):
    beatmapID = str(beatmapID)
    url = "https://osu.ppy.sh/api/get_beatmaps?k=" + apiKey + "&b=" + beatmapID
    response = requests.get(url)
    response = response.json()[0]
    return response

def getUser(userID):
    userID = str(userID)
    url = "https://osu.ppy.sh/api/get_user?k=" + apiKey + "&u=" + userID
    response = requests.get(url)
    response = response.json()
    return response

def getUserTop(userID, limit):
    userID = str(userID)
    limit = str(limit)
    url = "https://osu.ppy.sh/api/get_user_best?k=" + apiKey + "&u=" + userID + "&limit=" + limit
    response = requests.get(url)
    response = response.json()
    return response

def getUserRecent(userID, limit):
    userID = str(userID)
    limit = str(limit)
    url = "https://osu.ppy.sh/api/get_user_recent?k=" + apiKey + "&u=" + userID + "&limit=" + limit
    response = requests.get(url)
    response = response.json()
    return response

def getOsu(beatmapID):
    #cache/osu/beatmapID.osu
    beatmapID = str(beatmapID)
    url = "https://osu.ppy.sh/osu/{}".format(beatmapID)
    response = requests.get(url)
    if os.path.exists(cachePath + beatmapID + ".osu"):
        os.remove(cachePath + beatmapID + ".osu")
    
    with open(cachePath + beatmapID + ".osu", "w") as f:
        f.write(response.text)
    return True

def getUserID(username):
    username = str(username)
    url = "https://osu.ppy.sh/api/get_user?k=" + apiKey + "&u=" + username
    response = requests.get(url)
    response = response.json()
    return int(response[0]["user_id"])

def getUsername(userID):
    userID = str(userID)
    url = "https://osu.ppy.sh/api/get_user?k=" + apiKey + "&u=" + userID
    response = requests.get(url)
    response = response.json()
    return response[0]["username"]

def getAveragePPTOP(userID, limit):
    userID = str(userID)
    limit = str(limit)
    url = "https://osu.ppy.sh/api/get_user_best?k=" + apiKey + "&u=" + userID + "&limit=" + limit
    response = requests.get(url)
    response = response.json()
    pp = 0
    for i in response:
        pp += float(i["pp"])
    return pp / len(response)

def getBeatmapSet(beatmapSetID):
    beatmapSetID = str(beatmapSetID)
    url = "https://osu.ppy.sh/api/get_beatmaps?k=" + apiKey + "&s=" + beatmapSetID
    response = requests.get(url)
    response = response.json()
    return response