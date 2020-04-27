# -*- coding: utf-8 -*-
'''
@createBy  :   xiaowu 
@date    :   2019/10/22 14:09:28
'''
import multiprocessing
from lxml import etree
import re
import json
import traceback
import time

from xw_download_item import DownloaderItem

# 这是需要定制的部分，不同的网页 需要不同的解析
class Praser(multiprocessing.Process):

    # 从 htmlQueue 获取 html解析 然后放回 urlqueue 或者 item
    def __init__(self, htmlqueue, urlqueue, downloadqueue, itemqueue):
        multiprocessing.Process.__init__(self)
        self.htmlqueue = htmlqueue
        self.urlqueue = urlqueue
        self.downloadqueue = downloadqueue
        self.itemqueue = itemqueue
        # 对 hearthbuddy url数据加持
        self.totalPerClass = ['hunter','mage','neutral','paladin','priest','rogue','shaman','warlock','warrior']

    # 获取 html
    def __get_html(self):
        if(self.htmlqueue.empty()):
            return None
        else:
            html = self.htmlqueue.get()
            return html


    # 设置 url
    def __put_url(self,url):
        if(self.urlqueue.full()):
            print('urlqueue阻塞等待')
            time.sleep(2)
        self.urlqueue.put(url)

    # 设置 download_url
    def __put_download(self,download_url):
        if(self.downloadqueue.full()):
            print('downloadqueue阻塞等待')
            time.sleep(2)
        self.downloadqueue.put(download_url)

    # 设置 item,最好是字典对象
    def __put_item(self, item_dict):
        if(self.itemqueue.full()):
            print('itemqueue阻塞等待')
            time.sleep(2)
        self.itemqueue.put(item_dict)

    # 需要自定义的部分
    def __prase_doban_top(self):
        html = self.__get_html()
        if(html is not None):
            tree = etree.HTML(html)
            # 如果这三个是不同类型的 可以 优化
            # 将页面中 url放回, 这里涉及到url去重 todo
            

            # 获取自己想要的 文本数据
            cssselect = '#content > div > div.article > ol > li:nth-child({0})'
            # 循环 25 次
            try:
                # 获取自己想要的 资源
                pattern = re.compile(r'https://img.*jpg')
                # 在解析时 添加下载文件的名字
                # {'name':'砰然心动.jpg','download_url':"https://*****.jpg"}
                for match in pattern.finditer(html):
                    download_url = match.group(0)
                    download_url_split = download_url.strip().split('/')
                    # download_name = download_url_split[-1].split('.')[0].strip()
                    download_name = download_url_split[-1].strip()
                    download_item = DownloaderItem(download_name,download_url)
                    self.__put_download(download_item)

                for i in range(25):
                    data = tree.cssselect(cssselect.format(i+1))[0]
                    movie_info = {}
                    # 可能要判空
                    movie_info['name'] = (data.cssselect('div > div.info > div.hd > a > span:nth-child(1)'))[0].text
                    movie_info['score'] = float((data.cssselect('div > div.info > div.bd > div > span.rating_num'))[0].text)
                    movie_info['evaluateNumber'] = int((data.cssselect('div > div.info > div.bd > div > span:nth-child(4)'))[0].text[:-3])
                    info_str = (data.cssselect('div > div.info > div.bd > p:nth-child(1) > br'))[0].tail.strip()
                    info_str_split = info_str.split('/')
                    movie_info['year'] = info_str_split[0].strip()
                    movie_info['country'] = info_str_split[1].strip()
                    movie_info['type'] = info_str_split[2].strip()
                    movie_info['rank'] = int((data.cssselect('div > div.pic > em'))[0].text)
                    # movie_info['movieWord'] = (data.cssselect('div > div.info > div.bd > p.quote > span'))[0].text
                    self.__put_item(movie_info)
                
                # 将可能会报错的部分 放在最后 防止解释器问题

                # # 获取自己想要的 资源
                # pattern = re.compile(r'https://img.*jpg')
                # # 在解析时 添加下载文件的名字
                # # {'name':'砰然心动.jpg','download_url':"https://*****.jpg"}
                # for match in pattern.finditer(html):
                #     download_url = match.group(0)
                #     download_url_split = download_url.strip().split('/')
                #     # download_name = download_url_split[-1].split('.')[0].strip()
                #     download_name = download_url_split[-1].strip()
                #     download_item = DownloaderItem(download_name,download_url)
                #     self.__put_download(download_item)
            except:
                print('html 解析失败')

    def __prase_hearthbuddy(self):
        html_json = self.__get_html()
        if(html_json is not None):
            try:
                html_dict = json.loads(html_json)

                # url url存储队列
                # 第一次初始的时候就完成了 所有需要爬取的url
                data = {}
                # print(html_dict['nextPage'])
                if(html_dict['nextPage'] != 1):
                    # data = {'cardClass':'druid', 'standard':0, 'p':18, 't':1571913341021}
                    data['cardClass'] = html_dict['curCardClass']
                    data['standard'] = 0
                    data['p'] = html_dict['nextPage']
                    # print(data['p'])
                    data['t'] = 1571913341021
                    self.__put_url(data)
                else:
                    if (self.totalPerClass):
                        data['cardClass'] = self.totalPerClass.pop()
                        data['standard'] = 0
                        data['p'] = 1
                        data['t'] = 1571913341021
                        self.__put_url(data)
                
                # 错误出现最少
                # downloader 下载队列
                cards_list = html_dict['cards']
                for card in cards_list:
                    download_url = card['imageUrl']
                    download_url_split = download_url.strip().split('/')
                    name_split = download_url_split[-1].split('_')
                    name = '{0}_{1}_{2}'.format(card['cardCode'],card['cardClass'],name_split[-1])
                    downloader_item = DownloaderItem(name,download_url)
                    self.__put_download(downloader_item)

                

                # itemqueue 数据存储队列
                # 这里承担 数据清洗工作
                # BOT_565 Sim_BOT_565_xxx() 
                for card in cards_list:
                    hearth_info = {}
                    hearth_info['cardid'] = card['cardCode']
                    hearth_info['199_class'] = card['cardClass']
                    hearth_info['engname'] = card['code']
                    hearth_info['185_cardname']= card['name']
                    hearth_info['184_cardtextinhand'] = card['description']
                    hearth_info['203_rarity'] = card['cardRarity']
                    hearth_info['202_cardtype'] = card['cardType']
                    hearth_info['48_manacost'] = card['cost']
                    hearth_info['45_health'] = card['health']
                    hearth_info['47_attack'] = card['attack']
                    hearth_info['200_race'] = card['cardRace']
                    hearth_info['187_durability'] = card['durability']
                    hearth_info['cardEffect'] = card['cardEffect']
                    self.__put_item(hearth_info)

            except:
                traceback.print_exc()
                print('html_json 解析失败')
        # else:
        #     time.sleep(0.1)
        # 这样并没有退出
        # else:
        #     print('praser stop')
        #     exit()



    # 进程运行体
    def run(self):
        # time.sleep(1.1)
        print('praser run')
        while True:
            try:
                self.__prase_hearthbuddy()
            except:
                continue
    

