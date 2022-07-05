from cgitb import reset
from unittest import result
import mysql.connector
import os

def query(sql):
    db = mysql.connector.connect(
        host="localhost",
        user="osu",
        passwd="osu",
        database="osu"
    )
    cursor = db.cursor(buffered=True)
    cursor.execute(sql, multi=True)
    db.commit()
    db.close()
    return result

def initDB():
    with open(os.path.join("db.sql")) as f:
        sql = f.read()
        query(sql)

initDB()