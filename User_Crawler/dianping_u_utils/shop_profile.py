from selenium import webdriver
import re

class Shop(object):
    def __init__(self, driver, shopid):
        driver.get("http://www.dianping.com/shop/" + str(shopid))
        breadcrumb = driver.find_element_by_class_name("breadcrumb")
        tag_list = breadcrumb.find_elements_by_tag_name("a")
        classifier_1 = tag_list[-2]
        classifier_2 = tag_list[-1] #useless in many cases
        #print(classifier_1.text)
        #print(classifier_2.text)
        filter_shopname = re.compile(u"<a0:span class=\"shop\">(.*?)</a0:span>")
        filter_address = re.compile(u"<span title=\"(.*?)\" itemprop=\"street-address\" class=\"item\">")
        filter_star = re.compile(u"<span class=\"mid-rank-stars mid-str(.*?)\" title=")
        html = driver.page_source
        #print(len(filter_shopname.findall(html)))
        #print(len(filter_address.findall(html)))
        #print(len(filter_star.findall(html)))
        shopname = filter_shopname.findall(html)[0]
        address = filter_address.findall(html)[0]
        star = filter_star.findall(html)[0]
        #
        self.shopid = shopid
        self.shopname = shopname
        self.type = classifier_1.text
        self.address = address
        self.star = star
    
    def getdict(self):
        result = dict()
        result["shopid"] = self.shopid
        result["shopname"] = self.shopname
        result["type"] = self.type
        result["address"] = self.address
        result["star"] = self.star
        return result
    
    def getstr(self):
        result = "{\n"
        result += "    \"shopid\": \"" + self.shopid + "\",\n"
        result += "    \"shopname\": \"" + self.shopname + "\",\n"
        result += "    \"type\": \"" + self.type + "\",\n"
        result += "    \"address\": \"" + self.address + "\",\n"
        result += "    \"star\": " + self.star + "\n}"
        return result
