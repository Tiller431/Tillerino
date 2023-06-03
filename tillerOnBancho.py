#irc bot
from logger import log
import socket
import os
from dotenv import load_dotenv
from db import db
from beatmaps import mods as m
from beatmaps import maptypes as mt
from api import osu
import threading as t
from beatmaps import ow

load_dotenv()

botAcc = False
banchoUrl = "irc.ppy.sh"
banchoPort = 6667
banchoNick = os.getenv("BANCHO_USERNAME")
banchoPass = os.getenv("BANCHO_PASSWORD")


def init():
    global s
    s = socket.socket()
    s.connect((banchoUrl, banchoPort))
    log.debug("Connected to " + banchoUrl + ":" + str(banchoPort))
    banchoCMD(("PASS " + banchoPass + "\r\n").encode(), verbose=False)
    banchoCMD(("NICK " + banchoNick + "\r\n").encode(), verbose=False)
    log.debug("Logging in as " + banchoNick)

    # start web server
    webServerThread = t.Thread(target=webServer)
    webServerThread.start()

def banchoCMD(cmd, verbose=True):
    s.send(cmd)
    if verbose:
        log.debug("(SENT) " + cmd.decode())


def joinChannel(channel):
    banchoCMD(("JOIN " + channel + "\r\n").encode())

def sendMessage(username, message):
    banchoCMD(("PRIVMSG " + username + " :" + message + "\r\n").encode())
    log.debug("(SENT) PRIVMSG " + username + " :" + message + "\r\n")

def sendAction(username, message):
    banchoCMD(("PRIVMSG " + username + " :ACTION " + message + "\r\n").encode())

def webServer():
    from flask import Flask, request
    app = Flask(__name__)
    @app.route("/tiller", methods=["POST"])
    def tiller():
        aim = False
        speed = False
        sender = "Tiller"
        # get data from request
        data = request.get_json()
        # get data from json
        mapType = data["type"]
        mods = data["mods"]

        log.info("{}Reccommending map for {}...{}".format(log.Color.GREEN, sender, log.Color.RESET))
        userid = osu.getUserID(sender)

        #update user stats before reccommending
        db.updateUser(userid)
        if mapType == "aim":
            aim = True

        elif mapType == "speed":
            speed = True


        try:
            mods = m.modsToEnum(mods)
        except:
            print("Invalid mods")
            mods = None

        mapid, mods, numMaps = db.getRandomOWmap(userid, mods=mods)

        if numMaps == 0:
            sendMessage(sender, "You have played all of the maps in my database! Please check back later or request different mods for more maps!")
            return "OK"

        while not mt.isAim(mapid) and aim:
            mapid, mods, numMaps = db.getRandomOWmap(userid, mods=mods)
        
        while not mt.isSpeed(mapid) and speed:
            mapid, mods, numMaps = db.getRandomOWmap(userid, mods=mods)

        ppStats = db.getPP(mapid, mods)
        mapStats = osu.getBeatmap(mapid)
        msg = ""
        #Create message
        msg = "[https://osu.ppy.sh/beatmapsets/{}#osu/{} {} - {} [{}]] ".format(osu.getBeatmapSetID(mapid), mapid, mapStats["artist"], mapStats["title"], mapStats["version"])
        msg += "Mods: +{} ".format(m.readableMods(mods))
        msg += "PP: 95% > {}pp | 98% > {}pp | 100% > {}pp ".format(round(float(ppStats[1]), 2), round(float(ppStats[4]), 2), round(float(ppStats[7]), 2))

        # calc ow maps from lb on a new thread
        #t.Thread(target=ow.calcOWFromLB, args=(mapid,)).start()

        sendMessage(sender, msg)
        return "OK"
    
    app.run(host="0.0.0.0", port=5000)




def main():
    init()
    while True: 
        msg = s.recv(1024).decode().split("\n")
        for line in msg:
            if "QUIT" in line:
                continue
            if "#" in line:
                #ignore line
                continue
            if "PING" in line:
                banchoCMD('PONG \r\n'.encode(), verbose=False)
            if "372" in line:
                #print server banner
                #motd
                try:
                    line = line.split("-")[1]
                    log.info(line)
                    if "boat" in line:
                        log.info("{}Connected to Bancho!{}".format(log.Color.GREEN, log.Color.RESET))
                except:
                    pass
            if "PRIVMSG" in line:
                log.debug(line)
                sender = line.split("!")[0][1:]
                userid = osu.getUserID(sender)
                message = line.split(":", 1)[1]
                log.debug(sender + ": " + message)
                if not db.userExists(userid):
                    sendMessage(sender, 'HI! I\'m Tiller, a bot made by.. uhh... Tiller! I recreated "Tillerino" with the "PP Meta" and staying up to date as my #1 priorities. Type "!r" to get started! If you have any questions, suggestions, or issues, please feel free to add me on discord at Tiller#0727 and let me know! Thanks for using my bot and remember to plz enjoy game! :D (Please keep in mind that this bot is still under HEAVY development and there WILL be bugs/issues.)')
                    log.info("{}New user {} joined!{}".format(log.Color.RED, sender, log.Color.RESET))
                    db.createUser(userid, sender)
                
                if "!help" in message:
                    sendMessage(sender, "Just !r for now, but I'll be adding more commands soon!")

                if "ACTION" in message:
                    #/me is playing [https://osu.ppy.sh/beatmapsets/1269899#/3069847 THE ORAL CIGARETTES - Mou Ii kai? [AF's Insane (ft. sparxo)]] +Hidden +DoubleTime
                    mapid = message.split("[")[1].split("/")[4].split(" ")[0]
                    mods = message.split("+")[1:]
                    
                    #get pp
                    pp = db.getPP(mapid, mods)
                    
                    


                    log.debug(line)

                if "!r" in message:
                    speed = False
                    aim = False
                    log.info("{}Reccommending map for {}...{}".format(log.Color.GREEN, sender, log.Color.RESET))
                    userid = osu.getUserID(sender)
                    if not db.userExists(userid):
                        sendMessage(sender, 'HI! I\'m Tiller, a bot made by.. uhh... Tiller! I recreated "Tillerino" with the "PP Meta" and staying up to date as my #1 priorities. Type "!r" to get started! If you have any questions, suggestions, or issues, please feel free to add me on discord at Tiller#0727 and let me know! Thanks for using my bot and remember to plz enjoy game! :D (Please keep in mind that this bot is still under HEAVY development and there WILL be bugs/issues. I am working on improving it everyday so check back tomorrow if its broken today!)')
                        db.createUser(0, sender)
                        continue
                    #update user stats before reccommending
                    db.updateUser(userid)
                    if "speed" in message:
                        speed = True
                    if "aim" in message:
                        aim = True


                    try:
                        mods = m.modsToEnum(message)
                    except:
                        print("Invalid mods")
                        mods = None

                    mapid, mods, numMaps = db.getRandomOWmap(userid, mods=mods)

                    if numMaps == 0:
                        sendMessage(sender, "You have played all of the maps in my database! Please check back later or request different mods for more maps!")
                        continue

                    while not mt.isAim(mapid) and aim:
                        mapid, mods, numMaps = db.getRandomOWmap(userid, mods=mods)
                    
                    while not mt.isSpeed(mapid) and speed:
                        mapid, mods, numMaps = db.getRandomOWmap(userid, mods=mods)

                    ppStats = db.getPP(mapid, mods)
                    mapStats = osu.getBeatmap(mapid)
                    msg = ""
                    #Create message
                    msg = "[https://osu.ppy.sh/beatmapsets/{}#osu/{} {} - {} [{}]] ".format(osu.getBeatmapSetID(mapid), mapid, mapStats["artist"], mapStats["title"], mapStats["version"])
                    msg += "Mods: +{} ".format(m.readableMods(mods))
                    msg += "PP: 95% > {}pp | 98% > {}pp | 100% > {}pp ".format(round(float(ppStats[1]), 2), round(float(ppStats[4]), 2), round(float(ppStats[7]), 2))

                    # calc ow maps from lb on a new thread
                    t.Thread(target=ow.calcOWFromLB, args=(mapid,)).start()

                    sendMessage(sender, msg)





if __name__ == "__main__":
    main()