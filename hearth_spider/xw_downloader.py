# -*- coding: utf-8 -*-
'''
@createBy  :   xiaowu 
@date    :   2019/10/22 17:01:41
'''

import multiprocessing
import requests
import os
import traceback
import aiohttp
import asyncio
import time

class Downloader(multiprocessing.Process):

    # 需要 下载文件夹，将资源 下载在相关文件夹
    def __init__(self,downloadqueue,path):
        multiprocessing.Process.__init__(self)
        self.downloadqueue = downloadqueue
        self.path = path
        self.once_num = 32

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
                    download_content = requests.get(download_item.downloadUrl).content
                    with open(file_path,'wb') as f:
                        f.write(download_content)
                    # print(download_item.name,'下载完成')
            except:
                traceback.print_exc()
                print(download_item.name,'下载失败')
    
    
    async def __download_async_file(self):
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
                    async with aiohttp.ClientSession() as session:
                        async with session.get(download_item.downloadUrl, timeout=30) as response:
                            download_content = await response.read()
                            with open(file_path,'wb') as f:
                                f.write(download_content)
            except:
                traceback.print_exc()
                print(download_item.name,'下载失败')
    
    # 为了方便协程 我们
    # 我们重新设计 (自上而下的设计 自下而上的设计，模块设计，金字塔式，金字塔顶端是产品)
    # 顺序设计 （自下而上，从小到大）
    # 需求设计 （要这个，我需要什么；自上而下，按需设计）
    # 1. 获取下载连接
    # 我们一次 下载多少任务最佳呢 暂时设计为16个

    # 2. 组装 多个协程任务
    # 3. 下载图片

    # 自上而下设计
    # 1. 下载图片（找到等待点，也就是任务切换点）
    async def __download_content(self, download_url):
        async with aiohttp.ClientSession() as session:
            response = await session.get(download_url, timeout=30)
            content = await response.read()
            return content
    
    async def __content_to_file(self, download_item):
        content = await self.__download_content(download_item.downloadUrl)
        file_path = os.path.join(self.path, download_item.name)
        try:
            # 先判断是否 存在文件夹
            if(not os.path.exists(self.path)):
                os.makedirs(self.path)
            # 判断文件是否存在
            if(not os.path.exists(file_path)):
                with open(file_path,'wb') as f:
                    f.write(content)
        except:
            traceback.print_exc()
            print(download_item.name,'下载失败')
    
    # 将16个任务打包 
    # async def __zip_task(self):
    #     download_item_list = []
    #     for _ in range(self.once_num):
    #         download_item = self.__get_download()
    #         if(download_item is not None):
    #             download_item_list.append(download_item)

    #     tasks = [asyncio.ensure_future(self.__content_to_file(download_item)) for download_item in download_item_list]

        



    # 进程 运行体
    def run(self):
        # time.sleep(1.2)
        print('downloader run')
        while True:
            try:
                download_item_list = []
                for _ in range(self.once_num):
                    download_item = self.__get_download()
                    if(download_item is not None):
                        download_item_list.append(download_item)

                tasks = [asyncio.ensure_future(self.__content_to_file(download_item)) for download_item in download_item_list]
                loop = asyncio.get_event_loop()
                loop.run_until_complete(asyncio.wait(tasks))
            except:
                continue


    # def run(self):
    #     print('downloader run')
    #     loop = asyncio.get_event_loop()
    #     while True:
    #         try:
    #             # 这样简单的调用就是 顺序执行
    #             task = loop.create_task(self.__download_async_file())
    #             loop.run_until_complete(task)
    #         except:
    #             continue
    
    # def run(self):
    #     print('downloader run')
    #     while True:
    #         try:
    #             self.__download_to_file()
    #         except:
    #             continue