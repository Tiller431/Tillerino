# https://data.ppy.sh/2022_04_01_performance_osu_top_10000.tar.bz2
# https://data.ppy.sh/2022_04_01_performance_osu_random_10000.tar.bz2
import threading
import requests
import os
from db import db
import time


#for folder in score folders
#    for file in folder

for folder in os.listdir("score"):
    if "bz2" in folder:
        continue
    #print("score/" + folder + "/" + file)
    with open("score/" + folder + "/osu_scores_high.sql", "r") as f:
        try:
            for line in f:
                if "DROP TABLE" in line:
                    print(line)
                    continue
                #convert from osu db to our db
                if "INSERT INTO" in line:
                    scores = line.split("VALUES ")[1][1:].strip("\n").strip(");").split("),(")
                    def thread(scores):
                        for score in scores:
                            #score_id,beatmap_id,user_id,score,max_combo,rank,50_count,100_count,300_count,misses_count,gekis_count,katus_count,perfect,date,pp,replay,hidden,country
                            #convert to beatmapid,beatmap_setid,userid,scoreid,mods,pp
                            score = score.split(",")
                            scoreid = score[0]
                            beatmapid = score[1]
                            userid = score[2]
                            mods = score[13]
                            pp = score[15]
                            

                            db.saveScore(beatmapid,userid,scoreid,mods,pp,0)


                    
                    

        except Exception as e:
            print(e)
            pass

                
