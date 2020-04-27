# 中国大学排名定向爬虫(不扩展爬虫,只有一个url)
# 中国大学最好网
# http://www.zuihaodaxue.com/zuihaodaxuepaiming2017.html
# http://www.zuihaodaxue.com/zuihaodaxuepaiming2018.html
# 程序结构设计,封装模块,提高可读性
# step1:从网络上获取大学排名网页内容 getHTMLText()
# step2:提取网页内容中信息到合适的数据结构 fillUnivList()
# step3:利用数据结构展示并输出结果 printUnivList()

import bs4
import requests
from bs4 import BeautifulSoup


def getHTMLText(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""


def fillUnivList(ulist, html):
    soup = BeautifulSoup(html, "html.parser")
    for tr in soup.find('tbody').children:
        if isinstance(tr, bs4.element.Tag):  # 判定是否是标签类型,去除字符串类型的干扰
            tds = tr.find_all('td')  # 将td标签信息加到列表中
            # print(tds)
            # print(tds[0].string)
            ulist.append([tds[0].string, tds[1].string, tds[3].string])  # 写入的是一组
            # print(ulist)
    # pass  # 不做任何操作的字符


# format函数
def printUnivList(ulist, num):
    # 当中文字符宽度不够时,采用西文字符填充,中西文字符占用宽度不同
    # 将学校字段宽度增加成10
    tplt = "{0:^10}\t{1:{3}^10}\t{2:^10}"  # {3}学校排名填充空格时,采用format第四个参数填充
    # print("{:^10}\t{:^6}\t{:^10}".format("排名","学校名称","总分"))  #打印表头
    print(tplt.format("排名", "学校名称", "总分", chr(12288)))
    for i in range(num):
        u = ulist[i]
        print(tplt.format(u[0], u[1], u[2], chr(12288)))
        # print(u[1])
        # print(type(u[0]))
    # print("Suc"+str(num))


# 主函数
def main():
    uinfo = []  # 数组类型
    url = 'http://www.zuihaodaxue.com/zuihaodaxuepaiming2018.html'
    # 分别调取三个函数内容
    html = getHTMLText(url)
    fillUnivList(uinfo, html)
    printUnivList(uinfo, 20)  # 打印20个数据


if __name__ == '__main__':
    # uinfo = []  # 数组类型
    # url = 'http://www.zuihaodaxue.com/zuihaodaxuepaiming2018.html'
    # # 分别调取三个函数内容
    # html = getHTMLText(url)
    # fillUnivList(uinfo, html)
    # printUnivList(uinfo, 20)  # 打印20个数据
    main()

# utf-8, 采用中文字符的空格填充chr(12288)
