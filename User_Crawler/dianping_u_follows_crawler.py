# encoding: utf-8
import random
import time
from selenium import webdriver

class Connection(object):
    def __init__(self):
        super(Connection, self).__init__()
        self.follows = []

    def getstr(self):
        result = "{\n    \"followsID\": \n    [\n"
        if len(self.follows) == 0:
            result = result + "    \n    ]\n}"
            return result
        for fol in list(self.follows)[:-1]:
            result = result + "        \"" + str(fol) + '\",\n'
        result = result + "        \"" + str(list(self.follows)[-1]) + "\"\n    ]\n}"
        return result

def get_follows(ID, driver):
    url = "http://www.dianping.com/member/" + str(ID) + "/follows"
    driver.get(url)
    content = driver.page_source
    content = content.split("\n")
    follows_count = 0
    beginning_point = 0
    connection = Connection()
    for line in content:
        beginning_point = beginning_point + 1
        if line.find(u"follows\" title=\"\" class=\"cur\">关注(") != -1:
            follows_count = get_number(line, u"follows\" title=\"\" class=\"cur\">关注(", ")")
        if line.find("href=\"/member/") != -1 and line.find("fans") != -1:
            break
    pages = follows_count / 30
    for i in range(1, pages + 2):
        time.sleep(random.randint(3, 4))
        url = "http://www.dianping.com/member/" + str(ID) + "/follows?pg=" + str(i)
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
                connection.follows = connection.follows + [get_number(line, "href=\"/member/", "\"")]
    connection.follows = set(connection.follows)
    return connection

def get_number(line, pre, pos):
    i = line.find(pre)
    j = line.find(pos, i+len(pre))
    return int(line[i+len(pre):j])
