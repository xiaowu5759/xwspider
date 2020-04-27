# -*- coding: utf-8 -*-
'''
@createBy  :   xiaowu 
@date    :   2019/10/22 15:43:32
'''

import requests
from lxml import etree
import re
import os

url = 'https://movie.douban.com/top250?start=175&filter='
print(url)

ry = requests.get(url, timeout=30)
ry.raise_for_status()
ry.encoding = ry.apparent_encoding
html = ry.text
# print(html)
# 将 html源码存储
html_path = 'demo.html'
html_path = os.path.abspath(os.path.join(os.path.split(os.path.realpath(__file__))[0], html_path))

with open(html_path,'w',encoding='UTF-8') as htmlf:
    htmlf.write(html)
doc = etree.HTML(html)
cssselect = '#content > div > div.article > ol > li:nth-child({0})'
data = doc.cssselect(cssselect.format(23))[0]
# info_str = (data.cssselect('div.bd > p:nth-child(1) > br'))[0].tail.strip()
# info_str_split = info_str.split('/')
# print(info_str_split)
name = (data.cssselect('div > div.info > div.hd > a > span:nth-child(1)'))[0].text
print(name)

pattern = re.compile(r'https://img.*jpg')
# print(pattern)
for match in pattern.finditer(html):
    print(match.group(0))

# html_test = '<a href="https://movie.douban.com/subject/1292064/"><img width="100" alt="楚门的世界" src="https://img3.doubanio.com/view/photo/s_ratio_poster/public/p479682972.jpg" class=""></a>'
# html_test = 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p479682972.jpg'
# html_test = 'Its after 12 noon, do you know where your rooftops are? https://img3.doubanio.com/view/photo/s_ratio_poster/public/p479682972.jpg'
# data = re.findall(r'https://img.*jpg',html)
# print(len(data))
