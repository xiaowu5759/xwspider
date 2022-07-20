# -*- coding: utf-8 -*-
'''
@createBy  :   xiaowu 
@date    :   2019/10/22 17:01:48
'''
import multiprocessing
import os
import csv
import time

class Saver(multiprocessing.Process):

    # 入参 存储路径
    def __init__(self,itemqueue,path):
        multiprocessing.Process.__init__(self)
        # 同样存在 初始化问题
        self.init_flag = True
        self.itemqueue = itemqueue
        self.path = path

    # 获取 itemqueue
    def __get_item(self):
        # if(not self.itemqueue.empty()):
        #     return self.itemqueue.get()
        # else:
        #     return None
        if(self.itemqueue.empty()):
            return None
        else:
            return self.itemqueue.get()

    # 保存在 text 文件中
    def __save_to_text(self):
        # 不需要判断 是否存在
        # if(not os.path.exists(self.path)):
        item = self.__get_item()
        # print(item)
        if(item is not None):
            with open(self.path,'a',encoding='UTF-8') as f:
                line = ''
                # line = '{0}|{1}|{2}|{3}|{4}|{5}|{6}|{7}|{8}|{9}|{10}|{11}|{12}\n'.format(item['cardid'],item['199_class'],item['engname'],item['year'],item['country'],item['type'],item['rank'])
                f.write(line)

    # 保存在 csv 文件中
    # 暂时 不行
    def __save_to_csv(self):
        item = self.__get_item()
        if(item is not None):
            # print(item)
            with open(self.path,'a',newline='',encoding='UTF-8') as f:
                w = csv.DictWriter(f, item.keys())
                if(self.init_flag):
                    # print(item.keys())
                    w.writeheader()
                    self.init_flag = False
                else:
                    # print(item.values())
                    w.writerow(item)
        # else:
        #     time.sleep(1)

    # 保存到 mysql 数据库中
    def __save_to_mysql(self):
        pass

    # 进程 运行体
    def run(self):
        # time.sleep(1.2)
        print('saver run')
        while True:
            try:
                self.__save_to_csv()
            except:
                continue
7