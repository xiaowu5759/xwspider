# -*- coding: utf-8 -*-
'''
@createBy  :   xiaowu 
@date    :   2019/10/22 17:01:41
'''

import multiprocessing
import requests
import os
import traceback

class Downloader(multiprocessing.Process):

    # 需要 下载文件夹，将资源 下载在相关文件夹
    def __init__(self,downloadqueue,path):
        multiprocessing.Process.__init__(self)
        self.downloadqueue = downloadqueue
        self.path = path

    # 获取 downloadqueue 
    def __get_download(self):
        # if(not self.downloadqueue.empty()):
        #     return self.downloadqueue.get()
        # else:
        #     return None
        if(self.downloadqueue.empty()):
            return None
        else:
            return self.downloadqueue.get()

    # download
    def __download_to_file(self):
        header = {'Referer': 'https://www.douban.com/',
                'User-Agent':'ozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        download_item = self.__get_download()
        if(download_item is not None):
            # 关于文件的命名
            file_path = os.path.join(self.path, download_item.name)
            try:
                # 先判断是否 存在文件夹
                if(not os.path.exists(self.path)):
                    os.makedirs(self.path)
                # 判断文件是否存在
                if(not os.path.exists(file_path)):
                    download_file = requests.get(download_item.downloadUrl,headers=header).content
                    with open(file_path,'wb') as f:
                        f.write(download_file)
                    # print(download_item.name,'下载完成')
            except:
                traceback.print_exc()
                print(download_item.name,'下载失败')

            

    # 进程 运行体
    def run(self):
        print('downloader run')
        while True:
            try:
                self.__download_to_file()
            except:
                continue