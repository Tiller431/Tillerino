from db import db

def setSettings(setting, value):
    query = "UPDATE settings SET value = ? WHERE setting = ?"
    db.query(query, (value, setting))
    return


def getSettings(setting):
    query = "SELECT value FROM settings WHERE setting = ?"
    return db.query(query, (setting,))[0][0]

def getSettingsDict(discordid):
    query = "SELECT * FROM settings WHERE discordid = ?"
    return db.query(query, (discordid,))[0]
