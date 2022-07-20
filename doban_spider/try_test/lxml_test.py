# -*- coding: utf-8 -*-
'''
@createBy  :   xiaowu 
@date    :   2019/10/21 13:21:44
'''

import requests
from lxml import etree

url = 'https://movie.douban.com/explore#!type=movie&tag=%E7%BB%8F%E5%85%B8&sort=rank&page_limit=20&page_start=250'
url = 'https://item.jd.com/6733026.html'
print(url)
r = requests.get(url, timeout=30)
r.raise_for_status()
r.encoding = r.apparent_encoding
html = r.text
# print(html)  # <Response [200]>
# print(type(html)) # <class 'str'>
doc = etree.HTML(html)
# print(doc) # <class 'lxml.etree._Element'>

xpath = doc.xpath('/html/body/div[6]/div/div[2]/div[1]')
# print(xpath) # [<Element div at 0x15fc2bb8e88>]
print(xpath[0].get('class'))

css = doc.cssselect('body > div:nth-child(10) > div > div.itemInfo-wrap > div.sku-name')
# print(css[0].text) # [<Element div at 0x16c8e9d9fc8>]
print(etree.tostring(css[0]))