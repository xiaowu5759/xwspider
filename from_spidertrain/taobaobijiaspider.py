# 功能描述:获取淘宝搜索页面的信息,提取其中的商品名称和价格
# 理解:淘宝的搜索接口,翻页处理(核心问题)
# 技术路线:requests+re

# 分析url,书包
# https://s.taobao.com/search?q=%E4%B9%A6%E5%8C%85&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306
# https://s.taobao.com/search?q=%E4%B9%A6%E5%8C%85&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306
# https://s.taobao.com/search?q=%E4%B9%A6%E5%8C%85&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306&bcoffset=3&ntoffset=3&p4ppushleft=1%2C48&s=44
# https://s.taobao.com/search?q=%E4%B9%A6%E5%8C%85&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306&bcoffset=0&ntoffset=6&p4ppushleft=1%2C48&s=88
# 程序结构设计
# step1:提交商品搜索请求,循环获取页面  getHTMLText()
# step2:对于每个页面,提取商品名称和价格信息  parsePage()
# step3:将信息输出到屏幕上  printGoodList()

import re

import requests


def getHTMLText(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""


# 解析商品页面,核心代码
# 不采用beautifulsoup,对于script操作
def parsePage(ilt, html):
    try:
        # r''不需要转义字符
        plt = re.findall(r'"view_price":"[\d.]*"', html)  # \" 为键
        tlt = re.findall(r'"raw_title":".*?"', html)  # 最小匹配
        # plt=re.findall(r'"price":"[\d.]*"',html)  #\" 为键
        # tlt=re.findall(r'"title":".*?"',html)  #最小匹配
        # plt=re.findall(r'\"view_price\"\:\"[\d\.]*\"',html)  #\" 为键
        # tlt=re.findall(r'\"raw_title\"\:\".*?\"',html)  #最小匹配
        # print(len(plt))  #正确第一次36,第二次44
        # print(len(tlt))
        # num=0
        for i in range(len(plt)):
            # num=num+1
            # print(num)
            # print(len(plt))  #正确第一次36,第二次44
            # print(len(tlt))
            price = eval(plt[i].split(':')[1])  # eval将获得的字符串最外层的单引号和双引号去掉
            title = eval(tlt[i].split(':')[1])
            # 写入输出的列表对象中
            ilt.append([price, title])  # 这样获取的是一一对应的关系吗
    except:
        print("")


def printGoodList(ilt):
    # 定义一个打印形式的模板
    tplt = "{:4}\t{:8}\t{:16}"  # 长度为4,长度为8,长度为16
    print(tplt.format("序号", "价格", "商品名称"))  # 打印表头
    count = 0
    for g in ilt:  # 遍历列表
        count = count + 1
        print(tplt.format(count, g[0], g[1]))  # 弱类型的编程语言


def main():
    goods = "书包"
    depth = 2
    start_url = 'https://s.taobao.com/search?q=' + goods
    infoList = []  # 定义一个列表数据结构存储商品信息
    for i in range(depth):  # 从0开始,一共就0,1两页,range()函数
        try:
            url = start_url + '&s=' + str(44 * i)  # 将数字转换成字符串类型
            html = getHTMLText(url)
            # print(html)
            parsePage(infoList, html)
        except:
            continue
    printGoodList(infoList)


if __name__ == '__main__':
    main()
