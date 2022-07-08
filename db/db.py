import mysql.connector
import os
from api import osu
import random

db = mysql.connector.connect(
    host="localhost",
    user="osu",
    passwd="osu",
    database="osu"
)

def query(sql, *args):
    cursor = db.cursor(buffered=True)
    try:
        print("Query: {}\nArgs:{}".format(sql, args))
        cursor.execute(sql, args)
        db.commit()
    except mysql.connector.Error as err:
        print("Error: {}".format(err.msg))
        db.rollback()



def queryOne(sql, *args):
    cursor = db.cursor(buffered=True)
    try:
        print("Query: {}\nArgs:{}".format(sql, args))
        cursor.execute(sql, args)
        result = cursor.fetchone()
        print("Result: {}".format(result))
    except mysql.connector.Error as err:
        print("Error: {}".format(err))
        result = None
    db.commit()

    return result

def queryAll(sql, *args):
    cursor = db.cursor(buffered=True)
    try:
        print("Query: {}\nArgs:{}".format(sql, args))
        cursor.execute(sql, args)
        result = cursor.fetchall()
        print("Result: {}".format(result))
    except mysql.connector.Error as e:
        print("Error: {}".format(e))
        result = None
    db.commit()

    return result

def queryMultiLn(sql, *args):
    cursor = db.cursor(buffered=True)
    try:
        print("Query: {}\nArgs:{}".format(sql, args))
        cursor.execute(sql, args, multi=True)
        db.commit()
    except mysql.connector.Error as err:
        print("Error: {}".format(err.msg))
        db.rollback()

    
def initDB():
    sql = "CREATE TABLE IF NOT EXISTS users( userid INTEGER PRIMARY KEY, discordid BIGINT, username TEXT, current_pp FLOAT, topplay FLOAT, average_pp FLOAT);"
    query(sql)
    sql = "CREATE TABLE IF NOT EXISTS beatmaps( id INTEGER AUTO_INCREMENT, beatmapid INTEGER, beatmap_setid INTEGER, difficulty_name TEXT, stars REAL, mods TEXT, pp90 REAL, pp95 REAL, pp96 REAL, pp97 REAL, pp98 REAL, pp99 REAL, pp995 REAL, pp100 REAL, PRIMARY KEY (id));"
    query(sql)
    #overweighted tables (beatmapid, beatmap_setid, topplays, average_pp, overweight_score)
    sql = "CREATE TABLE IF NOT EXISTS overweighted( beatmapid INTEGER, beatmap_setid INTEGER, topplays INTEGER, average_pp REAL, overweight_score REAL, PRIMARY KEY (beatmapid));"
    #scores table (beatmapid, beatmap_setid, userid, scoreid, mods, pp, overwight_rank)
    sql = "CREATE TABLE IF NOT EXISTS scores( beatmapid INTEGER, beatmap_setid INTEGER, userid INTEGER, scoreid BIGINT, mods TEXT, pp FLOAT, overweight_rank INTEGER, PRIMARY KEY (scoreid));"
    query(sql)

def getBeatmap(beatmapID):
    sql = "SELECT * FROM beatmaps WHERE beatmapid = %s"
    result = queryAll(sql, beatmapID)
    return result

def getUser(userID):
    sql = "SELECT * FROM users WHERE userid = %s"
    result = queryOne(sql, userID)
    return result


def deleteBeatmap(beatmapID):
    sql = "DELETE FROM beatmaps WHERE beatmapid = %s"
    query(sql, beatmapID)

def saveBeatmapData(beatmapID, stars, mods, pp90, pp95, pp96, pp97, pp98, pp99, pp995, pp100):
    #(beatmapid, beatmap_setid, difficulty_name, stars, length, pp90, pp95, pp96, pp97, pp98, pp99, pp995, pp100)
    sql = "INSERT INTO beatmaps (beatmapid, beatmap_setid, difficulty_name, stars, mods, pp90, pp95, pp96, pp97, pp98, pp99, pp995, pp100) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    bmData = osu.getBeatmap(beatmapID)
    #print(bmData)
    query(sql, beatmapID, int(bmData["beatmapset_id"]), bmData["version"], stars, mods, pp90, pp95, pp96, pp97, pp98, pp99, pp995, pp100)

def getUIDfromDID(did):
    sql = "SELECT userid FROM users WHERE discordid = %s"
    try:
        result = queryOne(sql, did)
        return result[0]
    except:
        return None

def createUser(did, username):
    #(userid, discordid, username, current_pp, topplay, average_pp)
    userid = osu.getUserID(username)
    sql = "INSERT INTO users (userid, discordid, username, current_pp, topplay, average_pp) VALUES (%s, %s, %s, 0, 0, 0);"
    query(sql, userid, did, username)

def updateUser(username):
    userid = osu.getUserID(username)
    averageTop = osu.getAveragePPTOP(userid, 5)
    currentTop = float(osu.getUserTop(userid, 1)[0]["pp"])
    totalPP = float(osu.getUser(userid)[0]["pp_raw"])
    sql = "UPDATE users SET current_pp = %s, average_pp = %s, topplay = %s WHERE userid = %s"
    query(sql, totalPP, averageTop, currentTop, userid)

def isMapInDB(beatmapID, mods):
    sql = "SELECT * FROM beatmaps WHERE beatmapid = %s AND mods = %s"
    result = queryOne(sql, int(beatmapID), mods)
    if result is None:
        return False
    else:
        return True

def getOWmap(beatmapID):
    sql = "SELECT * FROM overweighted WHERE beatmapid = %s"
    result = queryOne(sql, beatmapID)
    return result

def isMapOW(beatmapid):
    sql = "SELECT * FROM overweighted WHERE beatmapid = %s"
    result = queryOne(sql, beatmapid)
    if result is None:
        return False
    else:
        return True

def updateOWscore(beatmapID):
    sql = "SELECT * FROM scores WHERE beatmapid = %s"
    result = queryAll(sql, beatmapID)
    if result is None:
        return False
    else:
        owVal = 0
        totalPP = 0
        numScores = len(result)
        for score in result:
            owVal += score[6]
            totalPP += score[5]
        if owVal > 0:
            owVal = owVal / numScores
        if totalPP > 0:
            totalPP = totalPP / numScores
        sql = "UPDATE overweighted SET overweight_score = %s, average_pp = %s, topplays = %s WHERE beatmapid = %s"
        query(sql, owVal, totalPP, numScores, int(beatmapID))
        return False

def getOWscore(scoreID):
    sql = "SELECT * FROM scores WHERE scoreid = %s"
    result = queryOne(sql, scoreID)
    if result is None:
        return False
    else:
        return result["overweight_rank"]

def saveOWmap(beatmapID):
    mapstats = osu.getBeatmap(beatmapID)
    sql = "INSERT INTO overweighted (beatmapid, beatmap_setid, topplays, average_pp, overweight_score) VALUES (%s, %s, 0, 0, 0);"
    query(sql, beatmapID, int(mapstats["beatmapset_id"]))

def saveScore(beatmapID, userID, scoreID, mods, pp, owRank):
    sql = "INSERT INTO scores (beatmapid, beatmap_setid, userid, scoreid, mods, pp, overweight_rank) VALUES (%s, %s, %s, %s, %s, %s, %s);"
    query(sql, beatmapID, int(osu.getBeatmap(beatmapID)["beatmapset_id"]), userID, scoreID, mods, pp, owRank)

def isScoreOW(scoreID):
    sql = "SELECT * FROM scores WHERE scoreid = %s"
    result = queryOne(sql, scoreID)
    if result is None:
        return False
    else:
        return True

def getRandomOWmap(userID):
    #randomly select a map from the database
    lower, upper = getUserPPrange(userID)
    #overweight_score is < 5
    sql = "SELECT * FROM overweighted WHERE overweight_score < 5 AND average_pp BETWEEN %s AND %s"
    result = queryAll(sql, lower, upper)
    if result is None:
        return False
    else:
        print(result[random.randint(0, len(result)-1)][0])
        return result[random.randint(0, len(result)-1)][0]

def getUserPPrange(userID):
    sql = "SELECT * FROM users WHERE userid = %s"
    result = queryOne(sql, userID)
    if result is None:
        return False
    else:
        return result[5] - 50, result[5] + 50