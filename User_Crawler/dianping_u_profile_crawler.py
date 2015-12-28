# encoding: utf-8
import random
import time
import re
from selenium import webdriver

class User(object):
    def __init__(self):
        super(User, self).__init__()
        self.data = {
            'ID' : 0,#用户ID
            'Gender' : 'unknown',#性别
            'Checkin' : -1,#签到
            'Reg_date' : {'Year':1990, 'Month':1, 'Day':1},#注册时间
            'Last_Login' : {'Year':1990, 'Month':1, 'Day':1},#最后登录
            'Birthday' : {'Year':1900, 'Month':1, 'Day':1},
            'Follows' : -1,#关注
            'Fans' : -1,#粉丝
            'EXP' : -1,#贡献值
            'Review' : -1,#点评
            'Wishlist' : -1,#收藏
            'Picture' : -1,#图片
            'Bangdan' : -1,#榜单
            'Post' : -1, #帖子
            'Province' : 'unknown'
        }

    def getstr(self):
        result = "{\n"\
        + '    \"ID\": \"' + str(self.data['ID']) + "\",\n"\
        + '    \"Gender\": \"' + self.data['Gender'] + "\",\n"\
        + '    \"Checkin\": ' + str(self.data['Checkin']) + ",\n"\
        + '    \"Reg_date\": \n    {\n'\
        + '        \"Year\": ' + str(self.data['Reg_date']['Year']) + ',\n'\
        + '        \"Month\": ' + str(self.data['Reg_date']['Month']) + ',\n'\
        + '        \"Day\": ' + str(self.data['Reg_date']['Day']) + "\n    },\n"\
        + '    \"Last_Login\": \n    {\n'\
        + '        \"Year\": ' + str(self.data['Last_Login']['Year']) + ',\n'\
        + '        \"Month\": ' + str(self.data['Last_Login']['Month']) + ',\n'\
        + '        \"Day\": ' + str(self.data['Last_Login']['Day']) + "\n    },\n"\
        + '    \"Birthday\": \n    {\n'\
        + '        \"Year\": ' + str(self.data['Birthday']['Year']) + ',\n'\
        + '        \"Month\": ' + str(self.data['Birthday']['Month']) + ',\n'\
        + '        \"Day\": ' + str(self.data['Birthday']['Day']) + "\n    },\n"\
        + '    \"Follows\": ' + str(self.data['Follows']) + ",\n"\
        + '    \"Fans\": ' + str(self.data['Fans']) + ",\n"\
        + '    \"EXP\": ' + str(self.data['EXP']) + ",\n"\
        + '    \"Review\": ' + str(self.data['Review']) + ",\n"\
        + '    \"Wishlist\": ' + str(self.data['Wishlist']) + ",\n"\
        + '    \"Picture\": ' + str(self.data['Picture']) + ",\n"\
        + '    \"Bangdan\": ' + str(self.data['Bangdan']) + ",\n"\
        + '    \"Province\": \"' + self.data['Province'] + "\",\n"\
        + '    \"Post\": ' + str(self.data['Post']) + "\n}"
        return result

def get_page(ID, driver):
    url = "http://www.dianping.com/member/" + str(ID)
    driver.get(url)
    user = User()
    content = driver.page_source
    filter_province = re.compile("<span class=\"user-groun\".*>(.*?)</span>")
    find_province = filter_province.findall(content)
    if len(find_province) > 0:
        user.data['Province'] = find_province[0]
    try:
        button = driver.find_element_by_id("J_UMoreInfo")
        button.click()
    except:
        hehe = 'hehe'
    content = driver.page_source.split("\n")
    user.data['ID'] = ID
    for line in content:
        if line.find("class=\"woman\"></i>") != -1:
            user.data['Gender'] = 'woman'
        if line.find("class=\"man\"></i>") != -1:
            user.data['Gender'] = 'man'
        if line.find(u">签到(") != -1:
            user.data['Checkin'] = get_number(line, u">签到(", ")")
        if line.find(u"注册时间：</span>") != -1:
            user.data['Reg_date'] = get_date(line, u"注册时间：</span>", "<")
        if line.find(u"最后登录：</span>") != -1:
            user.data['Last_Login'] = get_date(line, u"最后登录：</span>", "<")
        if line.find(u">生日：</em>") != -1:
            user.data['Birthday'] = get_date(line, u">生日：</em>", "<")
        if line.find(u"关注</span><strong>") != -1:
            user.data['Follows'] = get_number(line, u"关注</span><strong>", "<")
        if line.find(u"粉丝</span><strong>") != -1:
            user.data['Fans'] = get_number(line, u"粉丝</span><strong>", "<")
        if line.find(u"贡献值：</span><span id=\"J_col_exp\">") != -1:
            user.data['EXP'] = get_number(line, u"贡献值：</span><span id=\"J_col_exp\">", "<")
        if line.find(u">点评(") != -1:
            user.data['Review'] = get_number(line, u">点评(", ")")
        if line.find(u">收藏(") != -1:
            user.data['Wishlist'] = get_number(line, u">收藏(", ")")
        if line.find(u">图片(") != -1:
            user.data['Picture'] = get_number(line, u">图片(", ")")
        if line.find(u">榜单(") != -1:
            user.data['Bangdan'] = get_number(line, u">榜单(", ")")
            #It's difficult to translate "榜单"...
        if line.find(u">帖子(") != -1:
            user.data['Post'] = get_number(line, u">帖子(", ")")
    return user

def get_number(line, pre, pos):
    i = line.find(pre)
    j = line.find(pos, i+len(pre))
    return int(line[i+len(pre):j])

def get_date(line, pre, pos):
    i = line.find(pre)
    i = i + len(pre)
    pos1 = line.find('-', i+1)
    pos2 = line.find('-', pos1+1)
    pos3 = line.find(pos, pos2+1)
    return {'Year':int(line[i:pos1]), 'Month':int(line[pos1+1:pos2]), 'Day':int(line[pos2+1:pos3])}
