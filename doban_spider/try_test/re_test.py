# -*- coding: utf-8 -*-
'''
@createBy  :   xiaowu 
@date    :   2019/10/22 16:37:15
    正则表达式默认从左往右匹配。
    正则表达式默认是贪婪模式。
    正则表达式默认在匹配到了内容后，则终止匹配，不继续匹配。
    对同一个问题，编写的正则表达式不是唯一的！
'''

# 校验地址推荐 RegexBuddy RegexMagic
import re

# 创建re对象
pattern = re.compile(r'^[\u4e00-\u9fa5]+?')
str = '你好'
# 只返回第一个符合的对象
print(pattern.search(str))  # None # 你好

# 返回所有
ls=re.findall(r'([1-9])(\d{5})','BIT 100081 tsu100084')
# [('1', '00081'), ('1', '00084')] 分组返回对象里面是一个元组
print(ls)  #输出列表对象 ['100081', '100084']

# 当作分隔符
ls=re.split(r'[1-9]\d{5}','BIT 100081 tsu100084')
print(ls)  # ['BIT ', ' tsu', '']

# 替换
ls=re.sub(r'[1-9]\d{5}',':zipcode','BIT 100081 tsu100084')
print(ls) # BIT :zipcode tsu:zipcode

match=re.search(r'[1-9]\d{5}','BIT 100081')
if match:
    print(match.span())  # (4, 10)

# 实战返回 媒体url
# html_test = '<a href="https://movie.douban.com/subject/1292064/"><img width="100" alt="楚门的世界" src="https://img3.doubanio.com/view/photo/s_ratio_poster/public/p479682972.jpg" class=""></a>'
# html_test = 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p479682972.jpg'
html_test = 'Its after 12 noon, do you know where your rooftops are? https://img3.doubanio.com/view/photo/s_ratio_poster/public/p479682972.jpg'
data = re.findall(r'https://img.*jpg',html_test)
print(data) # len(data)