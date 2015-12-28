# encoding: utf-8
import random
import time
from selenium import webdriver

class Connection(object):
    def __init__(self):
        super(Connection, self).__init__()
        self.fans = []

    def getstr(self):
        result = "{\n    \"fansID\": \n    [\n"
        if len(self.fans) == 0:
            result = result + "    \n    ]\n}"
            return result
        for fan in list(self.fans)[:-1]:
            result = result + "        \"" + str(fan) + '\",\n'
        result = result + "        \"" + str(list(self.fans)[-1]) + "\"\n    ]\n}"
        return result

def get_fans(ID, driver):
    url = "http://www.dianping.com/member/" + str(ID) + "/fans"
    driver.get(url)
    content = driver.page_source
    content = content.split("\n")
    fans_count = 0
    beginning_point = 0
    connection = Connection()
    for line in content:
        beginning_point = beginning_point + 1
        if line.find(u"fans\" title=\"\" class=\"cur\">粉丝(") != -1:
            fans_count = get_number(line, u"fans\" title=\"\" class=\"cur\">粉丝(", ")")
        if line.find("href=\"/member/") != -1 and line.find("fans") != -1:
            break
    pages = fans_count / 30
    for i in range(1, pages + 2):
        time.sleep(random.randint(3, 4))
        url = "http://www.dianping.com/member/" + str(ID) + "/fans?pg=" + str(i)
        driver.get(url)
        content = driver.page_source
        content = content.split("\n")
        beginning_point = 0
        for line in content:
            beginning_point = beginning_point + 1;
            if line.find("href=\"/member/") != -1 and line.find("fans") != -1:
                break
        for line in content[beginning_point + 2:]:
            if line.find("href=\"/member/") != -1:
                connection.fans = connection.fans + [get_number(line, "href=\"/member/", "\"")]
    connection.fans = set(connection.fans)
    return connection

def get_number(line, pre, pos):
    i = line.find(pre)
    j = line.find(pos, i+len(pre))
    return int(line[i+len(pre):j])
