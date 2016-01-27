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

def getInRange(first, last, step):
    driver = webdriver.Firefox()
    for i in range(first, last+1, step):
        print(i)
        try:
            time.sleep(random.randint(3, 4))
            profile_str = dianping_u_profile_crawler.get_page(i, driver).getstr()
            if not profile_str.find("\"Year\": 1990") == -1:
                out = open("./status.txt", 'w')
                out.write(str(i) + "\n")
                out.close()
                continue
            out = codecs.open("./Data/%s_profile.txt"%str(i), 'w', 'utf-8')
            out.write(profile_str + "\n")
            out.close()
            ###
            # threshold
            file_threshold = open("./Data/%s_profile.txt"%str(i))
            content_json = json.loads(file_threshold.read())
            file_threshold.close()
            if content_json['Checkin'] <= 0 or content_json['Review'] <= 0:
                continue
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
            out = open("./status.txt", 'w')
            out.write(str(i))
            out.close()
        except:
            driver.close()
            raise
    driver.close()
