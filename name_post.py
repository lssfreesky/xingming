#W8 -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 11:48:43 2018

@author: S
"""
import requests
import json
import re
import xlwt
import time
import pandas as pd
from selenium import webdriver
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Chrome
from bs4 import BeautifulSoup
import urllib
#import urllib2
import urllib.request

# 姓
surname='宗'

################## 建立备选姓名列表 ###########################################
# 因为八字缺金火， 依八字选取了
# “9画属火+16画属金”、“9画属金+16画属火”和“19画属火+16画属金”、“19画属金+16画属火”的组合
# 笔画依据康熙字典笔画，和现代笔画不同
# 这里可以按自己具体需要修改
namelist=[];
m=1

# 组合 9-16
# 火 9
fire9={'炯','昭','炳','亮','炫'}
# 金 9
gold9={'钇'}
# 火 16
fire16={'烨','燃','晔'}
# 金 16
gold16={'锡','锜','铮','锖'}

print('9火+16金 备选姓名:')
for i in fire9:
    for j in gold16:
        name=i+j
        fullname=surname+name
        namelist.append(name)
        print(m, fullname)
        m=m+1

print('9金+16火 备选姓名:')            
for i in gold9:
    for j in fire16:
        name=i+j
        fullname=surname+name
        namelist.append(name)
        print(m, fullname)
        m=m+1
        
# 组合19-16
# 火 19
fire19={'烁'}
# 金 9
gold19={'锵','镗','铿'}
# 火 16
fire16={'烨','燃','晔'}
# 金 16
gold16={'锡','锜','铮','锖'}

print('19火+16金 备选姓名:')
for i in fire19:
    for j in gold16:
        name=i+j
        fullname=surname+name
        namelist.append(name)
        print(m, fullname)
        m=m+1

print('19金+16火 备选姓名:')           
for i in gold19:
    for j in fire16:
        name=i+j
        fullname=surname+name
        namelist.append(name)
        print(m, fullname)
        m=m+1       
################# 定义函数建立参数列表 #########################################
def gpara(name):
    params = {}
    params['data_type'] = "0"  # 0代表阳历，1代表阴历
    params['year'] = "2018"    #年
    params['month'] = "10"     #月
    params['day'] = "14"       #日
    params['hour'] = "7"       #时
    params['minute'] = "18"    #分
    params['pid'] = "浙江".encode('gb18030')    #省
    params['cid'] = "杭州".encode('gb18030')    #城市
    params['wxxy'] = "0"       #这个不知道是什么
    params['xing'] = surname.encode('gb18030') #姓
    params['ming'] = name.encode('gb18030')    #名
    params['sex'] = "1"        # 1代表男，0代表女
    params['act'] = "submit"
    params['isbz'] = "1"
    return params


################# 调取浏览器 ##################################################
# 用谷歌浏览器
driver = webdriver.Firefox()
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'}
#headers得根据自己的浏览器F12下自行修改调整
# 用火狐浏览器
#driver = Chrome() 
#headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
#headers得根据自己的浏览器F12下自行修改调整


################# 从网站爬取数据 ##############################################
datacon=pd.DataFrame()#建立dataframe存储循环中所有名字的数据
url2="http://life.httpcn.com/xingming.asp" #网址
for name in namelist:
    userinfo = dict() #建立dict存储循环中单个名字的数据
    params=gpara(name)                #建立表单参数
    userinfo['fullname']=surname+name #全名
    response = requests.post(url2, data = params, headers=headers)
    soup=BeautifulSoup(response.content, 'html.parser', from_encoding="gb18030")
    for node in soup.find_all("div", class_="chaxun_b"):
        node_cont = node.get_text()
        if u'姓名五格评分' in node_cont:
            name_wuge = node.find(string=re.compile(u" 姓名五格评分"))
            userinfo['wuge_score'] = node.find_all("b")[0].text #存储姓名五格评分
        if u'姓名八字评分' in node_cont:
            name_wuge = node.find(string=re.compile(u"姓名八字评分"))
            userinfo['bazi_score'] = node.find_all("b")[1].text#存储姓名八字评分
    #存储姓名五格和八字评分总分
    userinfo['totscore']= float(userinfo['bazi_score'])+float(userinfo['wuge_score'])
    data=pd.DataFrame([userinfo], columns=userinfo.keys())
    datacon= pd.concat([datacon,data])
    print(surname+name,', 姓名五格评分 ',userinfo['wuge_score'], '姓名八字评分', userinfo['bazi_score'])


datacon= datacon.sort_values('totscore')     #根据总分排序
datacon.to_csv('mingzi.csv')                 #存储结果到CSV文件中
#response.json()