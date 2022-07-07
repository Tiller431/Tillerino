import mysql.connector
import os
from api import osu

def query(sql, *args):
    db = mysql.connector.connect(
        host="localhost",
        user="osu",
        passwd="osu",
        database="osu"
    )
    cursor = db.cursor(buffered=True)
    try:
        print("Query: {}\nArgs:{}".format(sql, args))
        cursor.execute(sql, args)
        db.commit()
    except mysql.connector.Error as err:
        print("Error: {}".format(err.msg))
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
        print("Query: {}\nArgs:{}".format(sql, args))
        cursor.execute(sql, args)
        result = cursor.fetchone()
    except mysql.connector.Error as err:
        print("Error: {}".format(err))
        result = None
    db.commit()
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
        print("Query: {}\nArgs:{}".format(sql, args))
        cursor.execute(sql, args)
        result = cursor.fetchall()
    except mysql.connector.Error as e:
        print("Error: {}".format(e))
        result = None
    db.commit()
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
        print("Query: {}\nArgs:{}".format(sql, args))
        cursor.execute(sql, args, multi=True)
        db.commit()
    except mysql.connector.Error as err:
        print("Error: {}".format(err.msg))
        db.rollback()
    db.close()
    
def initDB():
    sql = "CREATE TABLE IF NOT EXISTS users( userid INTEGER PRIMARY KEY, discordid BIGINT, username TEXT, current_pp FLOAT, topplay FLOAT, average_pp FLOAT);"
    query(sql)
    sql = "CREATE TABLE IF NOT EXISTS beatmaps( id INTEGER AUTO_INCREMENT, beatmapid INTEGER, beatmap_setid INTEGER, difficulty_name TEXT, stars REAL, mods TEXT, pp90 REAL, pp95 REAL, pp96 REAL, pp97 REAL, pp98 REAL, pp99 REAL, pp995 REAL, pp100 REAL, PRIMARY KEY (id));"
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

