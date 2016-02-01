# encoding: utf-8
import time
import codecs
import os
import random
import json
import dianping_u_profile_crawler
import dianping_u_follows_crawler
import dianping_u_fans_crawler
import dianping_u_checkins_crawler
import dianping_u_reviews_crawler
from selenium import webdriver

def getInRange(inputfile):
    f=open(inputfile)
    ###
    # stores all IDs as a list, elements as int
    IDpool=[]    
    while 1:
        line=f.readline()
        line=str(line).strip('\n')
        if line: IDpool.append(int(line))
        else: break
    if len(IDpool)==0:
        print 'Error! Inputfile is empty!'
        raise
    ###
    for i in IDpool:
        print(i)
        driver = webdriver.Firefox()
        try:
            time.sleep(random.randint(3, 4))
            profile_str = dianping_u_profile_crawler.get_page(i, driver).getstr()
            if not profile_str.find("\"Year\": 1990") == -1:
                raise
            out = codecs.open("./Data/%s_profile.txt"%str(i), 'w', 'utf-8')
            out.write(profile_str + "\n")
            out.close()
            ###
            # threshold
            file_threshold = open("./Data/%s_profile.txt"%str(i))
            content_json = json.loads(file_threshold.read())
            file_threshold.close()
            if content_json['Checkin'] <= 0 or content_json['Review'] <= 0:
                raise
            ###
            print("... processing an active user ...")
            time.sleep(random.randint(3, 4))
            out = codecs.open("./Data/%s_follows.txt"%str(i), 'w', 'utf-8')
            out.write(dianping_u_follows_crawler.get_follows(i, driver).getstr() + "\n")
            out.close()
            time.sleep(random.randint(3, 4))
            out = codecs.open("./Data/%s_fans.txt"%str(i), 'w', 'utf-8')
            out.write(dianping_u_fans_crawler.get_fans(i, driver).getstr() + "\n")
            out.close()
            time.sleep(random.randint(3, 4))
            out = codecs.open("./Data/%s_checkins.txt"%str(i), 'w', 'utf-8')
            out.write(dianping_u_checkins_crawler.get_checkins(i, driver) + "\n")
            out.close()
            time.sleep(random.randint(3, 4))
            out = codecs.open("./Data/%s_reviews.txt"%str(i), 'w', 'utf-8')
            out.write(dianping_u_reviews_crawler.get_reviews(i, driver) + "\n")
            out.close()
            driver.close()
        except:
            driver.close()
            continue

