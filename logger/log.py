from dotenv import load_dotenv
import os
import time

load_dotenv()


debugConf = True if os.getenv("DEBUG").lower() == "true" else False
printDB = True if os.getenv("DEBUGDB").lower() == "true" else False
printAPI = True if os.getenv("DEBUGAPI").lower() == "true" else False

class Color:
    #console colors
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    DARKGREY = "\033[90m"
    RESET = "\033[0m"



def info(msg):
    #time - [INFO] - msg
    print(Color.CYAN + "{} - [INFO] - {}".format(time.strftime("%H:%M:%S"), msg) + Color.RESET)

def error(msg):
    #time - [ERROR] - msg
    print(Color.RED + "{} - [ERROR] - {}".format(time.strftime("%H:%M:%S"), msg) + Color.RESET)

def debug(msg):
    #time - [DEBUG] - msg
    debug = True
    if debug:
        print(Color.MAGENTA + "{} - [DEBUG] - {}".format(time.strftime("%H:%M:%S"), msg) + Color.RESET)

def db(msg):
    #time - [DB] - msg
    if printDB:
        print(Color.DARKGREY + "{} - [DB] - {}".format(time.strftime("%H:%M:%S"), msg) + Color.RESET)

def api(msg):
    #time - [API] - msg
    if printAPI:
        print(Color.GREEN + "{} - [API] - {}".format(time.strftime("%H:%M:%S"), msg) + Color.RESET)