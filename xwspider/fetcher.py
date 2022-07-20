# -*- coding: utf-8 -*-
'''
@author  :   xiaowu 
@date    :   2020/04/13 10:00:02
'''
class Fetcher(multiprocessing.Process):

    # 提高适用性，面向对象编程
    def __init__(self,proxiesqueue,urlqueue,htmlqueue):
        multiprocessing.Process.__init__(self)
        self.proxiesqueue = proxiesqueue
        self.urlqueue = urlqueue
        self.htmlqueue = htmlqueue

    def __get_urlqueue(self):
        pass

    def __put_htmlqueue(self):
        pass

