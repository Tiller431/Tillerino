import mysql.connector
from api import osu
import random
from logger import log
from beatmaps import mods as m
from beatmaps import calc


def query(sql, *args):
    db = mysql.connector.connect(
    host="localhost",
    user="osu",
    passwd="osu",
    database="osu"
)
    cursor = db.cursor(buffered=True)
    try:
        log.db("Query: {}\nArgs:{}".format(sql, args))
        cursor.execute(sql, args)
        db.commit()
        db.close()
    except mysql.connector.Error as err:
        log.error("Error: {}".format(err.msg))
        db.rollback()
        db.close()



def queryOne(sql, *args):
    db = mysql.connector.connect(
    host="localhost",
    user="osu",
    passwd="osu",
    database="osu"
)
    cursor = db.cursor(buffered=True)
    try:
        log.db("Query: {}\nArgs:{}".format(sql, args))
        cursor.execute(sql, args)
        result = cursor.fetchone()
        db.commit()
        db.close()
    except mysql.connector.Error as err:
        log.error("Error: {}".format(err))
        result = None
        db.close()


    return result

def queryAll(sql, *args):
    db = mysql.connector.connect(
    host="localhost",
    user="osu",
    passwd="osu",
    database="osu"
)
    cursor = db.cursor(buffered=True)
    try:
        log.db("Query: {}\nArgs:{}".format(sql, args))
        cursor.execute(sql, args)
        result = cursor.fetchall()
        db.commit()
        db.close()
    except mysql.connector.Error as e:
        log.error("Error: {}".format(e))
        result = None
        db.close()

    return result

def queryMultiLn(sql, *args):
    db = mysql.connector.connect(
    host="localhost",
    user="osu",
    passwd="osu",
    database="osu"
)
    cursor = db.cursor(buffered=True)
    try:
        log.db("Query: {}\nArgs:{}".format(sql, args))
        cursor.execute(sql, args, multi=True)
        db.commit()
        db.close()
    except mysql.connector.Error as err:
        log.error("Error: {}".format(err.msg))
        db.rollback()
        db.close()

    
def initDB():
    sql = "CREATE TABLE IF NOT EXISTS users( userid INTEGER PRIMARY KEY, discordid BIGINT, username TEXT, current_pp FLOAT, topplay FLOAT, average_pp FLOAT);"
    log.debug("Creating users table.")
    query(sql)
    sql = "CREATE TABLE IF NOT EXISTS beatmaps( id INTEGER AUTO_INCREMENT, beatmapid INTEGER, beatmap_setid INTEGER, difficulty_name TEXT, stars REAL, mods TEXT, pp90 REAL, pp95 REAL, pp96 REAL, pp97 REAL, pp98 REAL, pp99 REAL, pp995 REAL, pp100 REAL, PRIMARY KEY (id));"
    log.debug("Creating beatmaps table.")
    query(sql)
    #overweighted tables (beatmapid, beatmap_setid, topplays, average_pp, overweight_score)
    sql = "CREATE TABLE IF NOT EXISTS overweighted( id INTEGER AUTO_INCREMENT, beatmapid INTEGER, beatmap_setid INTEGER, mods BIGINT, topplays INTEGER, average_pp REAL, overweight_score REAL, PRIMARY KEY (id));"
    log.debug("Creating overweighted table.")
    query(sql)
    #scores table (beatmapid, beatmap_setid, userid, scoreid, mods, pp, overwight_rank)
    sql = "CREATE TABLE IF NOT EXISTS scores( beatmapid INTEGER, beatmap_setid INTEGER, userid INTEGER, scoreid BIGINT, mods TEXT, pp FLOAT, overweight_rank INTEGER, PRIMARY KEY (scoreid));"
    log.debug("Creating scores table.")
    query(sql)

def getBeatmap(beatmapID):
    sql = "SELECT * FROM beatmaps WHERE beatmapid = %s"
    log.debug("Getting beatmap {}".format(beatmapID))
    result = queryAll(sql, beatmapID)
    return result

def getUser(did):
    sql = "SELECT * FROM users WHERE discordid = %s"
    log.debug("Getting user {}".format(did))
    try:
        result = queryOne(sql, did)
    except:
        result = None
    return result


def deleteBeatmap(beatmapID):
    sql = "DELETE FROM beatmaps WHERE beatmapid = %s"
    log.debug("Deleting beatmap {}".format(beatmapID))
    query(sql, beatmapID)

def saveBeatmapData(beatmapID, stars, mods, pp90, pp95, pp96, pp97, pp98, pp99, pp995, pp100):
    #(beatmapid, beatmap_setid, difficulty_name, stars, length, pp90, pp95, pp96, pp97, pp98, pp99, pp995, pp100)
    sql = "INSERT INTO beatmaps (beatmapid, beatmap_setid, difficulty_name, stars, mods, pp90, pp95, pp96, pp97, pp98, pp99, pp995, pp100) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    bmData = osu.getBeatmap(beatmapID)
    #print(bmData)
    log.debug("Saving beatmap {} with mods {}".format(beatmapID, mods))
    query(sql, beatmapID, int(bmData["beatmapset_id"]), bmData["version"], stars, mods, pp90, pp95, pp96, pp97, pp98, pp99, pp995, pp100)

def getUIDfromDID(did):
    sql = "SELECT userid FROM users WHERE discordid = %s"
    try:
        log.debug("Getting userid from discordid {}".format(did))
        result = queryOne(sql, did)
        return result[0]
    except:
        return None

def createUser(did, username):
    #(userid, discordid, username, current_pp, topplay, average_pp)
    userid = osu.getUserID(username)
    sql = "INSERT INTO users (userid, discordid, username, current_pp, topplay, average_pp) VALUES (%s, %s, %s, 0, 0, 0);"
    log.debug("Creating user {} with discordid {}".format(username, did))
    query(sql, userid, did, username)

def updateUser(username):
    username = osu.getUserID(username)
    userid = osu.getUserID(username)
    averageTop = osu.getAveragePPTOP(userid, 5)
    currentTop = float(osu.getUserTop(userid, 1)[0]["pp"]) if osu.getUserTop(userid, 1)[0]["pp"] == 0 else averageTop
    totalPP = float(osu.getUser(userid)[0]["pp_raw"])
    mods = osu.getUserMods(userid)
    sql = "UPDATE users SET current_pp = %s, average_pp = %s, topplay = %s, mods = %s WHERE userid = %s"
    log.debug("Updating user: {}".format(username))
    query(sql, totalPP, averageTop, currentTop, mods, userid)

def changeUsername(did, username):
    userid = osu.getUserID(username)
    sql = "UPDATE users SET username = %s, userid = %s WHERE discordid = %s"
    log.debug("Changing username: {}".format(username))
    query(sql, username, userid, did)

def isMapInDB(beatmapID, mods):
    sql = "SELECT * FROM beatmaps WHERE beatmapid = %s AND mods = %s"
    log.debug("Checking if map {} is in DB with mods {}".format(beatmapID, mods))
    result = queryOne(sql, int(beatmapID), mods)
    if result is None:
        return False
    else:
        return True

def getOWmap(beatmapID, mods):
    sql = "SELECT * FROM overweighted WHERE beatmapid = %s AND mods = %s"
    log.debug("Getting OW map: {}".format(beatmapID))
    result = queryOne(sql, beatmapID, mods)
    return result

def isMapOW(beatmapid, mods):
    sql = "SELECT * FROM overweighted WHERE beatmapid = %s AND mods = %s"
    log.debug("Checking if map is in OW table: {}".format(beatmapid))
    result = queryOne(sql, beatmapid, mods)
    if result is None:
        return False
    else:
        return True

def updateOWscore(beatmapID, mods):
    sql = "SELECT * FROM scores WHERE beatmapid = %s AND mods = %s"
    log.debug("Updating OW beatmap: {}".format(beatmapID))
    result = queryAll(sql, beatmapID, mods)
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
        sql = "UPDATE overweighted SET overweight_score = %s, average_pp = %s, topplays = %s WHERE beatmapid = %s AND mods = %s"
        query(sql, owVal, totalPP, numScores, int(beatmapID), mods)
        return False

def getOWscore(scoreID):
    sql = "SELECT * FROM scores WHERE scoreid = %s"
    log.debug("Getting score {}".format(scoreID))
    result = queryOne(sql, scoreID)
    if result is None:
        return False
    else:
        return result["overweight_rank"]

def saveOWmap(beatmapID, mods):
    mapstats = osu.getBeatmap(beatmapID)
    sql = "INSERT INTO overweighted (beatmapid, beatmap_setid, mods, topplays, average_pp, overweight_score) VALUES (%s, %s, %s, 0, 0, 0);"
    log.debug("Saving BM to OW table: {}".format(mapstats["beatmap_id"]))
    query(sql, beatmapID, int(mapstats["beatmapset_id"]), mods)

def saveScore(beatmapID, userID, scoreID, mods, pp, owRank):
    sql = "INSERT INTO scores (beatmapid, beatmap_setid, userid, scoreid, mods, pp, overweight_rank) VALUES (%s, %s, %s, %s, %s, %s, %s);"
    log.debug("Saving score: {}".format(scoreID))
    query(sql, beatmapID, int(osu.getBeatmap(beatmapID)["beatmapset_id"]), userID, scoreID, mods, pp, owRank)

def isScoreOW(scoreID):
    sql = "SELECT * FROM scores WHERE scoreid = %s"
    log.debug("Checking if score is in DB: {}".format(scoreID))
    result = queryOne(sql, scoreID)
    try:
        if result[5] > 0:
            return True
        else:
            return False
    except:
        return False

def getRandomOWmap(userID, mods=None):
    #randomly select a map from the database
    lower, upper = getUserPPrange(userID)
    mods = osu.getUserMods(userID)

    sql = "SELECT * FROM overweighted WHERE average_pp >= %s AND average_pp <= %s AND (mods = %s OR mods = %s) AND overweight_score < 20"
    log.info("Getting random map between {} and {}".format(upper, lower, mods, 0))
    result = queryAll(sql, lower, upper, mods, mods + m.mods.HIDDEN)

    if len(result) == 0:
        sql = "SELECT * FROM overweighted WHERE average_pp >= %s AND average_pp <= %s"
        log.info("Getting random map between {}pp and {}pp for user {}.".format(lower, upper, userID))
        result = queryAll(sql, lower, upper)
        if len(result) == 0:
            return None, None, None
    log.debug("Got {} possible maps.".format(len(result)))
    #id INTEGER AUTO_INCREMENT, beatmapid INTEGER, beatmap_setid INTEGER, mods BIGINT, topplays INTEGER, average_pp REAL, overweight_score REAL
    mapNum = random.randint(0, len(result)-1)
    map = result[mapNum][1]
    mods = result[mapNum][3]
    log.debug("Sending map {}.".format(map))
    return map, mods, len(result)

def getUserPPrange(userID):
    sql = "SELECT * FROM users WHERE userid = %s"
    result = queryOne(sql, userID)
    if result is None:
        return False
    else:
        return result[5] - 25 if result[5] > 25 else 0, result[5] + 25

def getAllScores():
    sql = "SELECT * FROM scores"
    log.debug("Getting all scores.")
    result = queryAll(sql)
    return result

def getOWMods(beatmapID):
    sql = "SELECT * FROM overweighted WHERE beatmapid = %s"
    log.debug("Getting mods for map {}".format(beatmapID))
    result = queryOne(sql, beatmapID)
    if result is None:
        return False
    else:
        return result[3]


def getUserMods(userID):
    sql = "SELECT * FROM users WHERE userid = %s"
    log.debug("Getting mods for user {}".format(userID))
    result = queryOne(sql, userID)
    if result is None:
        return False
    else:
        return result[6]


def updateUserMods(userID, mods):
    sql = "UPDATE users SET mods = %s WHERE userid = %s"
    log.debug("Updating user {} with mods {}".format(userID, mods))
    query(sql, mods, userID)

def getPP(beatmapID, mods):
    sql = "SELECT * FROM beatmaps WHERE beatmapid = %s AND mods = %s"
    log.debug("Getting PP for map {}".format(beatmapID))
    result = queryOne(sql, beatmapID, m.readableMods(mods))
    log.debug("Got {}".format(result))
    if result is None:
        calc.calcPP(beatmapID)
        result = queryOne(sql, beatmapID, m.readableMods(mods))
    out = []
    for i in range(6, 14):
        out.append(result[i])

    return out

