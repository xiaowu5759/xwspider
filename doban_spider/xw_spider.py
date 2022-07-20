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
    url = 'https://movie.douban.com/top250'
    urlqueue = multiprocessing.Queue()
    htmlqueue = multiprocessing.Queue()
    downloadqueue = multiprocessing.Queue()
    itemqueue = multiprocessing.Queue()

    fetcher = Fetcher(url,urlqueue,htmlqueue)
    fetcher.start()

    praser = Praser(htmlqueue,urlqueue,downloadqueue,itemqueue)
    praser.start()

    download_path = 'image'
    download_path = os.path.abspath(os.path.join(os.path.split(os.path.realpath(__file__))[0], download_path))
    downloader = Downloader(downloadqueue,download_path)
    downloader.start()

    save_path = 'data.txt'
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
        time.sleep(10)
        if(urlqueue.empty() and fetcher.is_alive()):
            fetcher.terminate()
            print('fetcher stop')
        if(htmlqueue.empty() and praser.is_alive()):
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


