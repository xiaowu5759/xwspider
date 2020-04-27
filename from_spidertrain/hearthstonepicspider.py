# !/usr/bin/env python
# -*- coding:utf-8 -*-

# 功能描述：
# 目的：在炉石传说官网上的卡牌管理器上爬取卡牌图片，并分类保存
# 输入：无
# 输出：分类保存的图片文件
#
# 核心问题：处理网页上js效果，下载图片
# 优化思路：提供进度展示
# 技术路线：request，bs，re，selenium模拟
# 程序结构设计：
# step1：class HearthStone():设置全局变量，提供进度展示
# step2：hearthStoneSpider:启动模拟浏览器，触发js效果
# closeGuide
# step3：getPicList:bs煲汤，获取图片的地址
# step4：savePic:request下载保存图片，展示进度

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup as bs
import requests
import traceback
import time
import os


class HearthStone():
    # 保存全局变量
    def __init__(self):
        # 设置和启动模拟浏览器
        # options = Options()
        # options.add_argument('--headless')
        # options.add_argument('--disable-gpu')
        # self.driver = webdriver.Chrome(chrome_options=options)

        self.driver = webdriver.Chrome()
        # 记录开始时间
        self.time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # 一共需要爬取的图片数量
        self.end = 1
        # 已经下载的图片数量
        self.start = 0

    def hearthStoneSpider(self):
        # 获取首地址
        self.driver.get('https://hs.blizzard.cn/cards/')

        # 关闭引导界面
        firstBtn = self.driver.find_element_by_class_name("closeGuide")
        # 引导页面可能会出现错误,标签(炉石官方app)重合了，需要显示页面移动一下？
        self.driver.maximize_window()
        # 停留式，点击下一页
        ActionChains(self.driver).move_to_element(firstBtn).perform()
        time.sleep(1)
        ActionChains(self.driver).click(firstBtn).perform()
        time.sleep(1)

        # 切换到狂野界面
        # changeBtn=self.driver.find_element_by_class_name("mode_icon mode_standard")  #class name不行
        changeBtn = self.driver.find_element_by_xpath(
            '/html/body/div[3]/div/div[2]/div/div[1]/div/div[3]/div[2]/div[1]/div[2]/div[2]/ul/li[1]/a/span')
        ActionChains(self.driver).move_to_element(changeBtn).perform()
        time.sleep(1)
        ActionChains(self.driver).click(changeBtn).perform()
        time.sleep(1)
        # 对于触发按钮是和贴纸式可以使用xpath
        wildBtn = self.driver.find_element_by_xpath(
            '/html/body/div[3]/div/div[2]/div/div[1]/div/div[3]/div[2]/div[1]/div[2]/div[2]/ul/li[1]/a/ul/li[2]')
        ActionChains(self.driver).move_to_element(wildBtn).perform()
        time.sleep(1)
        ActionChains(self.driver).click(wildBtn).perform()
        time.sleep(1)

        # 更换九大职业
        for i in range(9):
            try:
                xPath = '/html/body/div[3]/div/div[2]/div/div[1]/div/div[3]/div[2]/div[1]/ul/li[' + str(i + 1) + ']/a'
                heroBtn = self.driver.find_element_by_xpath(xPath)
                ActionChains(self.driver).move_to_element(heroBtn).perform()
                time.sleep(1)
                ActionChains(self.driver).click(heroBtn).perform()
                time.sleep(1)

                # 如果下一页按钮显示，则一直按键
                while True:
                    # 获取下一页按钮
                    # nextBtn=self.driver.find_element_by_name("cards_next")
                    nextBtn = self.driver.find_element_by_css_selector('a[class="cards_next"]')
                    # 如果下一页隐藏就跳出来，从页面源码上直接匹配字段
                    if self.driver.page_source.find(
                            'class="cards_next" href="javascript:void(0);" style="display: none;"') != -1:
                        break
                    # 停留式，点击下一页
                    # ActionChains(self.driver).move_to_element(nextBtn).perform()
                    # time.sleep(1)
                    ActionChains(self.driver).click(nextBtn).perform()
                    # time.sleep(1)
                lst = self.getPicList(self.driver.page_source)
                self.end = len(lst) * 9
                self.savePic(lst)
            except:
                # try except 只仅对于循环
                #traceback.print_exc()  # 获得其中的错误信息
                continue

    def getPicList(self, html):
        # 新建一个列表
        lst = []
        soup = bs(html, 'lxml')
        # 将图片链接存入列表
        # srcs=soup.find_all('img',{'class':'imgload'})
        # srcs = soup.select('img[class="imgload"]')
        srcs = soup.select('.card_img')
        # print(type(srcs))
        # print(srcs)
        for i in range(len(srcs)):
            src = srcs[i]
            lst.append(src.attrs['src'])
        return lst

    def savePic(self, lst):
        for i in range(len(lst)):
            # 处理名字和地址
            name = lst[i].split('/')[-1]
            # print(name)
            fname = name.split('_')[2] + '_' + name.split('_')[3] + '_' + name.split('_')[5]  # 处理，一个列表
            froot = '/home/xiaowu/bear/hearthstone/' + name.split('_')[0] + '/'  # 绝对路径
            fpath = froot + fname
            try:
                if not os.path.exists(froot):
                    os.mkdir(froot)
                if not os.path.exists(fpath):
                    # 提交请求，下载处理
                    # print(lst[i])
                    r = requests.get(lst[i])
                    # r.raise_for_status()
                    with open(fpath, 'wb') as f:
                        f.write(r.content)
                # 把打印进度放在循环里面
                self.start += 1
                print('\r当前进度：{:.2f}%'.format(self.start * 100 / self.end), end='')  # \r能够打印的最后光标提到最前面
            except:
                #traceback.print_exc()  # 获得其中的错误信息
                print('爬取失败：' + fname)
                continue


if __name__ == '__main__':
    stone = HearthStone()
    print('开始时间：' + stone.time)
    stone.hearthStoneSpider()
    print('\r爬取结束：' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    stone.driver.quit()
    print('模拟浏览器关闭！')