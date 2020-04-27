# -*- coding: utf-8 -*-
'''
@createBy  :   xiaowu 
@date    :   2019/10/22 14:09:28
'''
import multiprocessing
from lxml import etree
import re

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

    # 获取 html
    def __get_html(self):
        # print('get html')
        # print(self.htmlqueue.emtpy())
        # if(not self.htmlqueue.emtpy()):
        #     html = self.htmlqueue.get()
        #     return html
        # else:
        #     # return 空 会导致错误 无限死循环？
        #     print('kong')
        #     return None
        if(self.htmlqueue.empty()):
            # print('empty') # 输入 empty
            return None
        else:
            html = self.htmlqueue.get()
            # print('get html')
            return html


    # 设置 url
    def __put_url(self,url):
        
        self.urlqueue.put(url)
        # print(url)

    # 设置 download_url
    def __put_download(self,download_url):
        # print(download_url)
        self.downloadqueue.put(download_url) 

    # 设置 item,最好是字典对象
    def __put_item(self, item_dict):
        # print(item_dict)
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

    # 进程运行体
    def run(self):
        # 避免去重问题
        print('praser run')
        for i in range(25,250,25):
            url = 'https://movie.douban.com/top250?start={0}&filter='.format(i)
            self.__put_url(url)
            # print(url)
        while True:
            try:
                self.__prase_doban_top()
            except:
                continue


