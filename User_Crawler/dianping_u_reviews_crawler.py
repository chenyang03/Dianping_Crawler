# encoding: utf-8
import random
import time
import codecs
import re
from selenium import webdriver
from dianping_u_utils.shop_profile import *

class Reviews(object):
    def __init__(self):
        super(Reviews, self).__init__()
        self.reviews = []

    def getstr(self):
        result = "{\n"
        result = result + "    \"count\": " + str(len(self.reviews)) + ",\n"
        result = result + "    \"reviews\": \n    [\n"
        if len(self.reviews) == 0:
            result = result + "    \n    ]\n}"
            return result
        for i in range(len(self.reviews)-1):
            result = result + "        {\n            \"date\": \"" + self.reviews[i][4] + '\",\n            \"shopName\": \"' + self.reviews[i][1] + "\",\n" + "            \"shopID\": \"" + self.reviews[i][0] + "\",\n" + "            \"stars\": " + str(self.reviews[i][2]) + ",\n" + "            \"comments\": \"" + self.reviews[i][3] + '\"\n        },\n'
        result = result + "        {\n            \"date\": \"" + self.reviews[len(self.reviews)-1][4] + '\",\n            \"shopName\": \"' + self.reviews[len(self.reviews)-1][1] + "\",\n" + "            \"shopID\": \"" + self.reviews[len(self.reviews)-1][0] + "\",\n" + "            \"stars\": " + str(self.reviews[len(self.reviews)-1][2]) + ",\n" + "            \"comments\": \"" + self.reviews[len(self.reviews)-1][3] + '\"\n        }\n    ]\n}'
        return result

def get_reviews(ID, driver):
    url = "http://www.dianping.com/member/" + str(ID) + "/reviews"
    driver.get(url)
    content = driver.page_source
    reviews_count = 0
    reviews = Reviews()
    
    #get reviews_count
    filter_count = re.compile(u">点评\((.*?)\)<")
    if len(filter_count.findall(content)) != 0:
        reviews_count = int(filter_count.findall(content)[0])
    
    pages = reviews_count / 15
    for i in range(1, pages + 2):
        time.sleep(random.randint(3, 4))
        url = "http://www.dianping.com/member/" + str(ID) + "/reviews?pg=" + str(i)
        driver.get(url)
        content = driver.page_source
        #crawl reviews into lists
        filter_nameId = re.compile("Tracker._trackPageview\('dp_myreviews_shopname'\);\" title=\"\" class=\"J_rpttitle\" href=\"http://www.dianping.com/shop/(.*?)\">(.*?)</a></h6>")
        filter_star = re.compile("<div class=\"mode-tc comm-rst\">(.*?)</div>", re.S)
        filter_comment = re.compile("<div class=\"mode-tc comm-entry\">(.*?)</div>")
        filter_date = re.compile(u"<span class=\"col-exp\">.*?于(.*?)</span>")
        nameId = filter_nameId.findall(content)
        star = filter_star.findall(content)
        rank_star = re.compile("class=\"item-rank-rst irr-star(.*?)\"")
        for i in range(len(star)):
            tmp = rank_star.findall(star[i])
            if len(tmp) == 0:
                star[i] = 11
            else:
                star[i] = int(tmp[0])
        comment = filter_comment.findall(content)
        date = filter_date.findall(content)
        #save lists into Reviews
        for i in range(0, len(nameId)):
            temp = []
            temp.append(nameId[i][0])
            #print("shopID: ", nameId[i][0])
            temp.append(nameId[i][1])
            temp.append(int(star[i]))
            temp.append(comment[i])
            temp.append(date[i])
            reviews.reviews.append(temp)
        # store shop profiles
        for each_id in nameId:
            try:
                testf = open("./Data/Shops/" + str(each_id[0]))
                testf.close()
                continue
            except:
                "do nothing ..."
            time.sleep(random.randint(3, 4))
            try:
                print("now getting " + str(each_id[0]))
                s = Shop(driver, str(each_id[0]))
                outf = codecs.open("./Data/Shops/" + str(each_id[0]), 'w', 'utf-8')
                outf.write(s.getstr() + "\n")
                outf.close()
            except:
                continue
    return reviews.getstr()
