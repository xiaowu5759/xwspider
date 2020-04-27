# 介绍,编写,优化
# 如何优化,提高用户体验
# 提升速度,动态显示进度

# 功能描述:
# 目标:获取上交所和深交所所有股票名称和交易信息
# 输入:
# 输出:保存到文件中

# 技术路线:request,bs4,re
# 理解:思路的可行性

# 分析网站url
# 新浪股票: http://finance.sina.com.cn/stock/
# 百度股票: http://gupiao.baidu.com/stock/
# 候选数据网站的选择
# 选取原则: 股票数据信息静态存在与html页面中,非js代码生成,没有robots协议限制
# 由后台服务器将数据写在代码中,由前台浏览器解析得来; 由前台浏览器通过js脚本获得的

# 百度网站不能包含所有股票信息
# 东方财富 http://quote.eastmoney.com/stocklist.html 包含所有的上交和深交所的股票代码

# 程序结构设计:
# step1: 从东方财富网获取股票列表  getHTMLText(url),getStockList(lst,stockURL)
# step2: 根据股票列表逐个到百度股票获取个股信息  getStackInfo(lst,stockURL,fpath)
# step3: 将结果存储到文件中
# 数据结构分析:字典类型是维护键值对的数据

import re

import requests
from bs4 import BeautifulSoup as bs


# 速度提高:编码识别优化
def getHTMLText(url, code='utf-8'):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = code
        return r.text
    except:
        return ""


# def getHTMLText(url):
#     try:
#         r=requests.get(url)
#         r.raise_for_status()
#         r.encoding=r.apparent_encoding  #程序动态执行会浪费一定时间
#         return r.text
#     except:
#         return ""

def getStockList(lst, stockURL):
    html = getHTMLText(stockURL, 'GB2312')
    soup = bs(html, 'html.parser')
    # a=soup.find_all('a')  #得到的是一个遍历类型ResultSet
    # quote = soup.find_all('div', attrs={'id': 'quotesearch'})  # 得到的是一个ResultSet类型,可以用来遍历的
    quote = soup.find('div', attrs={'id': 'quotesearch'})  # 得到的是一个Tag类型
    count = 0
    for child in quote.descendants:
        # print(type(child))  #遍历有各种各样的类型
        # print(child)
        # 以下这句话不行
        # if type(child)=='bs4.element.Tag':
        #     print(child)
        if child.name == 'a':
            count = count + 1
            if count > 3:
                try:
                    href = child.attrs['href']
                    sign = re.findall(r'[s][hz]\d{6}', href)
                    # if not sign==[]:
                    #     lst.append(sign)  #在链接中找到不同点
                    #     print(lst)
                    lst.append(sign[0])  # 这里0的作用是取列表里的值
                except:
                    return ""
    # print(lst)  #这里为什么无打印结果

    # a=child.find_all('a')  #只搜索一层?
    # print(type(a))
    # for i in a:
    #     #利用正则表达式进行筛选
    #     try:
    #         href=i.attrs['href']  #所有a标签的链接域中
    #         #print(href)
    #         #print(type(re.findall(r'[s][hz]\d{6}',href)))  #返回一个列表类型,默认空列
    #         lst.append(re.findall(r'[s][hz]\d{6}',href))  #在链接中找到不同点
    #         #print(type(lst))
    #         #print(lst)
    #     except:
    #         return ""


def getStockInfo(lst, stockURL, fpath):
    count = 0

    # stock=lst[230]
    # url = stockURL + stock + '.html'
    # html = getHTMLText(url)
    # # print(html)
    # infoDict = {}  # 利用字典类型数据结构,作为过渡
    # soup=bs(html,'html.parser')
    # stockInfo=soup.find('div',attrs={'class':'stock-bets'})
    # name = stockInfo.find_all(attrs={'class': 'bets-name'})  #这里类型是bs4.element.ResultSet,就是一大堆集合
    # name = stockInfo.find_all(attrs={'class': 'bets-name'})[0]  #这里类型就是Tag
    # 为了稳定性,其实也没有改变什么,应该和html页面自身有关
    # name = stockInfo.find(attrs={'class': 'bets-name'})
    # print(name)
    # print(name.text)
    # print(name.string)

    for stock in lst:
        url = stockURL + str(stock) + '.html'  # 取值之后就不需要
        # url=stockURL+stock+'.html'  #需要类型转换
        html = getHTMLText(url)
        try:
            if html == "":
                continue
            infoDict = {}  # 利用字典类型数据结构,作为过渡
            soup = bs(html, 'html.parser')
            stockInfo = soup.find('div', attrs={'class': 'stock-bets'})
            name = stockInfo.find(attrs={'class': 'bets-name'})
            infoDict.update({'股票名称': name.text.split()[0]})  # 这里要用text,不能用String,String返回None
            # 寻找键值对
            keyList = stockInfo.find_all('dt')  # 键的域,是一个集合类型Set
            valueList = stockInfo.find_all('dd')  # 值的域
            # 还原键值对,并将其赋予到字典中
            for i in range(len(keyList)):  # 集合里的长度
                key = keyList[i].text
                val = valueList[i].text
                infoDict[key] = val  # 这里字典的用法
            # 将字典保存到文件中
            with open(fpath, 'a', encoding='utf-8') as f:  # with会自动关闭文件,不需要close
                f.write(str(infoDict) + '\n')  # 转换数据类型
                # f.close()
                # print("文件保存成功")
                count = count + 1  # 执行之后会换行的进度条
                print('\r当前进度:{:.2f}%'.format(count * 100 / len(lst)), end='')  # \r能够打印的最后光标提到最前面
        except:
            count = count + 1  # 执行之后会换行的进度条
            print('\r当前进度:{:.2f}%'.format(count * 100 / len(lst)), end='')  # \r能够打印的最后光标提到最前面
            # traceback.print_exc()  #获得其中的错误信息
            continue
    f.close()
    print("文件保存成功")


def main():
    stock_list_url = 'http://quote.eastmoney.com/stocklist.html'
    stock_info_url = 'https://gupiao.baidu.com/stock/'
    output_file = '/home/xiaowu/bear/BaiduStockInfo2.txt'  # 文件保存路径
    slist = []  # 股票列表
    getStockList(slist, stock_list_url)
    # print(slist)
    getStockInfo(slist, stock_info_url, output_file)


if __name__ == '__main__':
    main()
