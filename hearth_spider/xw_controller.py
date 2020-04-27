# -*- coding: utf-8 -*-
'''
@createBy  :   xiaowu 
@date    :   2019/10/23 14:48:19
'''
import multiprocessing
import time

class Controller(multiprocessing.Process):

    def __init__(self,urlqueue,htmlqueue,downloadqueue,itemqueue,fetcher,praser,downloader,saver):
        multiprocessing.Process.__init__(self)
        self.urlqueue = urlqueue
        self.htmlqueue = htmlqueue
        self.downloadqueue = downloadqueue
        self.itemqueue = itemqueue
        self.fetcher = fetcher
        self.praser = praser
        self.downloader = downloader
        self.saver = saver

    def run(self):
        while True:
            print('spider working')
            time.sleep(2)
            if(self.urlqueue.empty()):
                self.fetcher.terminate()
                print('fetcher stop')
            if(self.htmlqueue.empty()):
                self.praser.terminate()
                print('praser stop')
            if(self.downloadqueue.empty()):
                self.downloader.terminate()
                print('downloader stop')
            if(self.itemqueue.empty()):
                self.saver.terminate()
                print('saver stop')
            if(self.urlqueue.empty() and self.htmlqueue.empty() and self.downloadqueue.empty() and self.itemqueue.empty()):
                print('spider stop')
                exit()

