# -*- coding: utf-8 -*-
'''
@author  :   xiaowu 
@date    :   2020/04/16 17:25:01
'''
class Parser(multiprocessing.Process):

    def __init__(self,proxiesqueue,urlqueue,htmlqueue):
        multiprocessing.Process.__init__(self)
        self.itemqueue = itemqueue
        self.htmlqueue = htmlqueue
        self.urlqueue = urlqueue

    def __put_urlqueue(self):
        pass

    def __get_htmlqueue(self):
        pass