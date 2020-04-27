#!/usr/bin/env python
# -*- coding:utf-8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs
import traceback
import time
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.action_chains import ActionChains

# 定义一个爬取类
class Douyu():
    # 便于保存全局变量
    def __init__(self):
        # 设置和定义浏览器
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        self.driver=webdriver.Chrome(chrome_options=options)

        # options = FirefoxOptions()
        # options.add_argument('--headless')
        # self.driver = webdriver.Firefox(firefox_options=options)

        # self.driver=webdriver.PhantomJS()

        # self.driver = webdriver.Firefox()  #火狐浏览器鼠标动作链不可以，perfrom（）报错

        #self.driver=webdriver.Chrome()
        # 记录主播数量
        self.num=0
        # 记录观看的总人数
        self.count=0
        # 设置开始的全局时间
        self.time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # 已保存多少条信息
        self.start=0
        # 总共需要保存的信息
        self.end=1

    def douyuSpider(self):
        self.driver.get('https://www.douyu.com/directory/all')
        soup = bs(self.driver.page_source, 'lxml')
        end = soup.find_all('a',{'class':'shark-pager-item'})
        self.end = int(end[-1].text) * 120
        print('总共页数:'+end[-1].text+'\t'+str(self.end))

        lives = soup.find('div', {'id': 'live-list-content'})
        names = lives.select('span[class="dy-name ellipsis fl"]')
        numbers = lives.select('span[class="dy-num fr"]')
        if len(numbers) < len(names):
            tlen = len(names) - len(numbers)
            while tlen > 0:
                numbers.append('0')
                tlen -= 1
        for i in range(len(names)):
            name = names[i].text
            if isinstance(numbers[i], str):
                number = numbers[i]
            else:
                number = numbers[i].text
            self.num += 1
            # 格式化字段,存储
            tplt = '{0:^8}\t观众人数:{2:8}\t主播名:{1:{3}<10}'  # 填充空格
            self.saveFile(tplt.format(self.num, name, number, chr(12288)))
            if number[-1] == '万':
                countNum = float(number[:-1]) * 10000
            else:
                countNum = float(number)
            self.count += countNum
        # 新建一个字典
        # douyuDict={}
        while True:
        #for i in range(1):
            try:
                # 先点击，在操作，如果出错也是先点击，而不是再处理一次
                # 一直点击下一页
                if self.driver.page_source.find("shark-pager-next shark-pager-disable shark-pager-disable-next") != -1:
                    break
                # 如果不是最后一页就点击下一页
                # time.sleep(1)
                # self.driver.find_element_by_class_name("shark-pager-next").click()

                # next=self.driver.find_element_by_class_name("shark-pager-next")
                # actions = ActionChains(self.driver)
                # actions.move_to_element(next)
                # time.sleep(1)
                # actions.click(next)
                # time.sleep(1)

                nextBtn=self.driver.find_element_by_class_name("shark-pager-next")
                ActionChains(self.driver).move_to_element(nextBtn).perform()
                time.sleep(1)
                ActionChains(self.driver).click(nextBtn).perform()
                time.sleep(1)

                soup = bs(self.driver.page_source, 'lxml')
                # end = soup.find_all('a', {'class': 'shark-pager-item'})
                # self.end=int(end[-1].text)*120
                #选择字典类型使有对应关系
                lives=soup.find('div',{'id':'live-list-content'})
                # print(type(lives))  #一个tag类型
                # print(type(bs(str(lives),'lxml')))  #soup类型
                # 对于返回'bs4.element.ResultSet'如何处理
                names=lives.select('span[class="dy-name ellipsis fl"]')
                numbers=lives.select('span[class="dy-num fr"]')
                # 还原键值对,赋值到字典中
                # 字典不好存储
                # print(len(names))
                # print(len(numbers))  #出现列表不等情况
                if len(numbers) < len(names):
                    tlen=len(names)-len(numbers)
                    while tlen > 0:
                        #numbers.append('<span class="dy-num fr>0</span>')
                        numbers.append('0')
                        tlen-=1
                for i in range(len(names)):
                    #print(names[i])
                    name=names[i].text

                    if isinstance(numbers[i],str):
                        number = numbers[i]
                    else:
                        number = numbers[i].text

                    #number=numbers[i].text
                    #douyuDict[name]=number
                    #格式化字段,存储
                    self.num += 1
                    tplt='{0:^8}\t观众人数:{2:8}\t主播名:{1:{3}<10}'  #填充空格
                    self.saveFile(tplt.format(self.num,name,number,chr(12288)))
                    if number[-1]=='万':
                        countNum=float(number[:-1]) * 10000
                    else:
                        countNum = float(number)
                    self.count += countNum
                # # 主播名,返回列表
                # names = soup.find_all('span', {'class': 'dy-name ellipsis fl'})  # 配置一个字典类型
                # # 观众人数,返回列表
                # numbers = soup.find_all('span', {'class': 'dy-num fr'})
                # for name, number in zip(names, numbers):  # zip打包成元组
                #     tName = name.get_text().strip()
                #     tNumber = number.get_text().strip()
                #     self.saveFile('房间名:' + tName, '\t观众人数:' + tNumber)
                #     self.num += 1
                #     if tNumber[-1] == '万':
                #         countNum = float(tNumber[:-1]) * 10000
                #     else:
                #         countNum = float(tNumber)
                #     self.count += countNum

            except:
                #traceback.print_exc()  # 获得其中的错误信息
                continue  # 继续执行循环
            # finally:
            #     self.driver.close()
        self.saveFile('当前网站直播人数'+str(self.num)+'\t当前网站观众人数'+str(self.count))
        self.saveFile(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))




    def saveFile(self,str):
        fname='DouyuData'+self.time
        fpath='/home/xiaowu/bear/'+fname
        with open(fpath,'a',encoding='utf-8') as f:
            f.write(str+'\n')
            self.start+=1
            # 打印进度
            print('\r当前进度:{:.2f}%'.format(self.start*100/self.end),end='')  #\r能够打印的最后光标提到最前面

# 主程序
if __name__ == '__main__':
    d=Douyu()
    d.douyuSpider()
    print(time.strftime("\n%Y-%m-%d %H:%M:%S", time.localtime())+ '\t爬取完成!')
    # d.driver.close()  # 关闭当前页面
    d.driver.quit()  # 关闭并退出浏览器
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'\t浏览器关闭!')