# encoding: utf-8
from selenium import webdriver
from dianping_u_utils.shop_profile import *
import codecs
import re
import time
import random

def toJSON(times, places, shopID):
    result = "{\n"
    result = result + "    \"count\": " + str(len(times)) + ",\n"
    result = result + "    \"checkins\": \n    [\n"
    if len(times) == 0:
        result = result + "    \n    ]\n}"
        return result
    for i in range(0, len(times)-1):
        result = result + "        {\n            \"time\": \"" + times[i] + '\",\n            \"place\": \"' + places[i] + "\",\n" + "            \"shopID\": \"" + shopID[i] + '\"\n        },\n'
    result = result + "        {\n            \"time\": \"" + times[-1] + '\",\n            \"place\": \"' + places[-1] + "\",\n" + "            \"shopID\": \"" + shopID[-1] + '\"\n        }\n    ]\n}'
    return result

def get_checkins(ID, driver):
    driver.get("http://www.dianping.com/member/" + str(ID) + "/checkin")
    for i in range(1,200):
        try:
            button = driver.find_element_by_id("J_more")
            button.click()
        except:
            break
    html = driver.page_source
    filter1_time = re.compile(u"<span class=\"time\">(.{,14})\u5728</span>\n")
    filter1 = re.compile(r"<a title=\"\" target=\"_blank\" onclick=\"pageTracker[.]_trackPageview.*?;\" href=\"/shop/[0-9]*\">(.*?)</a>")
    filter1_shopID = re.compile(r"<a title=\"\" target=\"_blank\" onclick=\"pageTracker[.]_trackPageview.*?;\" href=\"/shop/([0-9]*)\">.*?</a>")
    filter2_time = re.compile(u"<span class=\"time\">(.{,14})\u5728</span><a title=\".*?\" target=\"_blank\" href=\"/shop/")
    filter2 = re.compile(u"<span class=\"time\">.{,14}\u5728</span><a title=\"(.*?)\" target=\"_blank\" href=\"/shop/")
    filter2_shopID = re.compile(u"lass=\"time\">.{,14}\u5728</span><a title=\".*?\" target=\"_blank\" href=\"/shop/([0-9]*)\"")
    times = filter1_time.findall(html) + filter2_time.findall(html)
    places= filter1.findall(html) + filter2.findall(html)
    shopID = filter1_shopID.findall(html) + filter2_shopID.findall(html)
    #print("shopID: ", shopID)
    for each_id in shopID:
        try:
            testf = open("./Data/Shops/" + str(each_id))
            testf.close()
            continue
        except:
            "do nothing ..."
        time.sleep(random.randint(3, 4))
        try:
            s = Shop(driver, str(each_id))
            outf = codecs.open("./Data/Shops/" + str(each_id), 'w', 'utf-8')
            outf.write(s.getstr() + "\n")
            outf.close()
        except:
            continue
    if not len(times) == len(places) or not len(places) == len(shopID):
        print("Something wrong...")
    return toJSON(times, places, shopID)
