# -*- coding: utf-8 -*-
'''
@createBy  :   xiaowu 
@date    :   2019/10/24 18:34:11
'''

import requests
import os
import json

url = 'https://hs.blizzard.cn/action/cards/query'

# cardClass=druid&p=2&standard=0&keywords=&t=1571913341021&cardSet=
data = {'cardClass':'druid', 'standard':0, 'p':1, 't':1571913341021}
response = requests.post(url,data=data)
# print(response.text)
demo_path = 'demo.json'
demo_path = os.path.abspath(os.path.join(os.path.split(os.path.realpath(__file__))[0], demo_path))
# with open(demo_path,'w',encoding='UTF-8') as f:
#     f.write(response.text)
html_dict = json.loads(response.text)
print(type(html_dict['cards'][1]))
# 打印下一页
print(html_dict['nextPage'])