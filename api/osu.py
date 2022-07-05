import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

apiKey = os.getenv("OSU_API_KEY")

def getBeatmap(beatmapID):
    url = "https://osu.ppy.sh/api/get_beatmaps?k=" + apiKey + "&b=" + beatmapID
    response = requests.get(url)
    response = response.json()
    return response

def getUser(userID):
    url = "https://osu.ppy.sh/api/get_user?k=" + apiKey + "&u=" + userID
    response = requests.get(url)
    response = response.json()
    return response

def getUserTop(userID, limit):
    url = "https://osu.ppy.sh/api/get_user_best?k=" + apiKey + "&u=" + userID + "&limit=" + limit
    response = requests.get(url)
    response = response.json()
    return response


