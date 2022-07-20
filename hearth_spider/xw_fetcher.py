# -*- coding: utf-8 -*-
'''
@createBy  :   xiaowu 
@date    :   2019/10/22 14:06:27
'''

import requests
import multiprocessing
import traceback
import time

class Fetcher(multiprocessing.Process):

    # 第一步 初始化 url
    # 不断的从 urlQueue 中获取 url
    def __init__(self,init_url,urlqueue,htmlqueue):
        self.init_flag = True
        multiprocessing.Process.__init__(self)
        self.init_url = init_url
        self.urlqueue = urlqueue
        self.htmlqueue = htmlqueue

    def __get_url(self):
        if(self.urlqueue.empty()):  # 单词写错了 ，也不报错？
            return None
        else:
            url = self.urlqueue.get()
            print('get url:',url)
            return url
            

    def __put_html(self,html):
        if(self.urlqueue.full()):
            print('urlqueue阻塞等待')
            time.sleep(2)
        self.htmlqueue.put(html)


    # 这里是 io密集型 可以优化
    def __fetch_get(self):
        header = {'Referer': 'https://www.douban.com/',
                'User-Agent':'ozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        # 判断是否 是第一次爬取
        # 放进 urlqueue ,但是取不出来
        # print('enter')
        if(self.init_flag):
            # print('init url')
            url = self.init_url
            self.init_flag = False
        else:
            # print('from urlqueue')
            
            url = self.__get_url() # 这里 出来问题？
            # print(self.init_flag)
            # print(url)
        
        if(url is not None):
            # print(url)
            try:
                response = requests.get(url, headers=header, timeout=30)
                response.raise_for_status()
                response.encoding = response.apparent_encoding
                # print(response.text)
                self.__put_html(response.text)
            except:
                # traceback.print_exc()
                print(url,'爬取页面失败')
    
    def __fetch_post(self):
        if(self.init_flag):
            url_data = self.init_url
            self.init_flag = False
            print('init url:',url_data)
        else:
            url_data = self.__get_url()

        if(url_data is not None):
            url = 'https://hs.blizzard.cn/action/cards/query'
            try:
                response = requests.post(url, data=url_data,timeout=30)
                response.raise_for_status()
                response.encoding = response.apparent_encoding
                self.__put_html(response.text)
            except:
                print(url_data,'爬取失败')
        # else:
        #     print('fetcher stop')
        #     exit()
            


    # 进程运行体
    def run(self):
        # time.sleep(1)
        print('fetcher run')
        while True:
            try:
                self.__fetch_post()
            except:
                continue

            

    