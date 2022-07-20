# -*- coding: utf-8 -*-
'''
@createBy  :   xiaowu 
@date    :   2019/10/22 15:34:35
'''

import multiprocessing
import os
import time

from xw_fetcher import Fetcher
from xw_praser import Praser
from xw_downloader import Downloader
from xw_saver import Saver
from xw_controller import Controller


if __name__ == "__main__":
    url_data = {'standard':0,'cardClass':'druid','p':1,'t':1571913341021}
    urlqueue = multiprocessing.Queue(100)
    htmlqueue = multiprocessing.Queue(100)
    # 就算设置成100 也会出现download阻塞等待
    # 因为sleep 2 
    # downloadqueue urlqueue itemqueue
    # 会出现 :
    # downloadqueue阻塞等待
    # fetcher stop
    # praser stop
    # saver stop
    # spider working
    # downloader stop
    # spider stop
    downloadqueue = multiprocessing.Queue(100)
    itemqueue = multiprocessing.Queue(100)

    fetcher = Fetcher(url_data,urlqueue,htmlqueue)
    fetcher.start()

    praser = Praser(htmlqueue,urlqueue,downloadqueue,itemqueue)
    praser.start()

    download_path = 'image'
    download_path = os.path.abspath(os.path.join(os.path.split(os.path.realpath(__file__))[0], download_path))
    downloader = Downloader(downloadqueue,download_path)
    downloader.start()

    save_path = 'data.csv'
    save_path = os.path.abspath(os.path.join(os.path.split(os.path.realpath(__file__))[0], save_path))
    saver = Saver(itemqueue,save_path)
    saver.start()

    # 新建控制 线程对象 的元组
    # 出现报错
    # control_process = []
    # control_process.append(fetcher)
    # control_process.append(praser)
    # control_process.append(downloader)
    # control_process.append(saver)
    # controller = Controller(urlqueue,htmlqueue,downloadqueue,itemqueue,fetcher,praser,downloader,saver)
    # controller.start()
    while True:
        print('spider working')
        time.sleep(128)  # 这个等待时间也就是 下载器 下载资源需要的时间
        # 这里的等待时间 也影响着爬取器 fetcher和praser的平衡

        # 主要是避免拥塞发生
        # 这样简单的判断可能不行，可能协程还在工作
        # 可能还在工作的问题
        # if(urlqueue.empty() and fetcher.is_alive()):
        #     fetcher.terminate()
        #     print('fetcher stop')

        # fetcher 爬取一个 然后 praser 解析一个
        # 现在总是停下来了
        # 就是其中一个速度不够
        if(urlqueue.empty() and fetcher.is_alive() and htmlqueue.empty() and praser.is_alive()):
            fetcher.terminate()
            print('fetcher stop')
            praser.terminate()
            print('praser stop')
        
        if(downloadqueue.empty() and downloader.is_alive()):
            downloader.terminate()
            print('downloader stop')
        if(itemqueue.empty() and saver.is_alive()):
            saver.terminate()
            print('saver stop')
        if(urlqueue.empty() and htmlqueue.empty() and downloadqueue.empty() and itemqueue.empty()):
            print('spider stop!')
            break

    # 将所有进程加入主进程
    fetcher.join()
    praser.join()
    downloader.join()
    saver.join()
    exit()


