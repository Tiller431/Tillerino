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
        cursor.execute(sql, args)
        print("Query: {}".format(sql))
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
        cursor.execute(sql, args, multi=True)
        print("Query: {}".format(sql))
        db.commit()
    except mysql.connector.Error as err:
        print("Error: {}".format(err.msg))
        db.rollback()
    db.close()
    
def initDB():
    with open(os.path.join("db.sql")) as f:
        sql = f.read()
        queryMultiLn(sql)

def getBeatmap(beatmapID):
    sql = "SELECT * FROM beatmaps WHERE beatmap_id = %s"
    result = queryAll(sql, beatmapID)
    return result

def getUser(userID):
    sql = "SELECT * FROM users WHERE user_id = %s"
    result = queryOne(sql, userID)
    return result

def getUserTop(userID, limit):
    sql = "SELECT * FROM user_top WHERE user_id = %s LIMIT %s"
    result = queryAll(sql, userID, limit)
    return result

def deleteBeatmap(beatmapID):
    sql = "DELETE FROM beatmaps WHERE beatmap_id = %s"
    query(sql, beatmapID)

def saveBeatmapData(beatmapID, mods, pp90, pp95, pp96, pp97, pp98, pp99, pp995, pp100):
    #(beatmapid, beatmap_setid, difficulty_name, stars, length, pp90, pp95, pp96, pp97, pp98, pp99, pp995, pp100)
    sql = "INSERT INTO beatmaps (beatmapid, beatmap_setid, difficulty_name, stars, mods, pp90, pp95, pp96, pp97, pp98, pp99, pp995, pp100) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    bmData = osu.getBeatmap(beatmapID)
    #print(bmData)
    query(sql, beatmapID, int(bmData["beatmapset_id"]), bmData["version"], float(bmData["difficultyrating"]), mods, pp90, pp95, pp96, pp97, pp98, pp99, pp995, pp100)
