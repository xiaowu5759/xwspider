
import requests
from bs4 import BeautifulSoup
import multiprocessing
import time
import os
 
# 进程1获取网页真实地址并存入队列中
class geturl(multiprocessing.Process):
    def __init__(self, urlqueue, count, url):
        multiprocessing.Process.__init__(self)
        self.urlqueue = urlqueue
        self.url = url
        self.count = count
 
    def run(self):
        # time.sleep(5)
        while self.count >= 0 and self.count <= 250:
            page_url = self.url + '?start=' + str(self.count) + '&filter='
            self.urlqueue.put(page_url)
            # self.urlqueue.task_done()
            self.count += 25
          #  time.sleep(1)
 
# 进程2获取信息并存入TXT文档中
class getcontent(multiprocessing.Process):
    def __init__(self, urlqueue):
        multiprocessing.Process.__init__(self)
        self.urlqueue = urlqueue
 
    def run(self):
        while True:
            header = {'Referer': 'https://www.douban.com/',
                      'User-Agent':
                          'ozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
            url = self.urlqueue.get()
            res = requests.get(url, headers=header)
            soup = BeautifulSoup(res.text, 'html.parser')
            for contents in soup.select('.info'):
                if contents.select('.hd') != []:
                    titles = ''.join(contents.select('.hd')[0].text.split())
                    # print(titles)
                if contents.select('.bd p') != []:
                    peoples = contents.select('.bd p')[0]
                    name = peoples.contents[0].strip()
                    addrs = peoples.contents[2].strip()
                    # print(name)
                    # print(addrs)
                score = contents.select('.bd .star .rating_num')[0].text
                numbers = contents.select('.bd .star span')[3].text  # .contents[6]
                # print (score)
                # print(numbers)
                if contents.select('.bd .quote .inq') != []:
                    message = contents.select('.bd .quote .inq')[0].text
                    # print(message)
 
                content = [titles, name, addrs,
                           score, numbers, message]
 
                with open('C:\\Users\\dell\\Desktop\\douban.txt', 'a', encoding='utf-8') as file:
                    for each in content:
                        file.write(each)
 
                        file.write('\n')
                    file.write('\n')
                    file.write('\n')
                # print()
 
            time.sleep(1)
 
 
# 进程3监控进程1，2
class contrl(multiprocessing.Process):
    def __init__(self, urlqueue):
        multiprocessing.Process.__init__(self)
        self.urlqueue = urlqueue
 
    def run(self):
        while True:
            print("程序执行中")
            time.sleep(60)
            if (self.urlqueue.empty()):
                print("程序执行完毕！")
                exit()
 
if __name__ == '__main__':
    url = 'https://movie.douban.com/top250'
    count = 0
    urlqueue = multiprocessing.Queue()
 
    t1 = geturl(urlqueue, count, url)
    t1.start()
 
    t2 = getcontent(urlqueue)
    t2.start()
 
    t3 = contrl(urlqueue)
    t3.start()