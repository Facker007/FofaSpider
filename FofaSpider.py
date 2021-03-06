# !/usr/bin/env python
# coding: utf-8

import sys
import re
import time
import base64
import random
import optparse
import requests

from urllib.parse import quote
from lxml import etree

def banner():
    print("""\033[36m
         _____      __       ____        _     _           
        |  ___|__  / _| __ _/ ___| _ __ (_) __| | ___ _ __ 
        | |_ / _ \| |_ / _` \___ \| '_ \| |/ _` |/ _ \ '__|
        |  _| (_) |  _| (_| |___) | |_) | | (_| |  __/ |   
        |_|  \___/|_|  \__,_|____/| .__/|_|\__,_|\___|_|
                                  |_|                   \033[0m                             
         # coded by KpLi0rn   website www.wjlshare.xyz
    """)


def cmd():
    parser = optparse.OptionParser()
    parser.add_option('-q', '--query', dest='query', help='write the query you want')
    parser.add_option('-r',dest='source',help='you txt path')   # 批量搜索文件
    parser.add_option('-p',dest='startpage',default=1,type=int,help='input the StartPage')
    parser.add_option('-s',dest='spidernum',default=0,type=int,help='intput the Spider number')
    (options, args) = parser.parse_args()
    return options,args

class FofaSpider(object):

    # query 就是我们的查询语句
    def __init__(self,Cookie,query,startpage,spidernum):
        self.q = quote(query)
        self.qbase64 = quote(str(base64.b64encode(query.encode()),encoding='utf-8'))
        self.UserAgent = ["Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0","Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36","Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11","Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16","Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36","Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)","Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)","Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50","Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0","Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11","Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)"]
        self.Cookie = Cookie
        self.header = {"User-Agent": random.choice(self.UserAgent), "Cookie": self.Cookie}
        self.page = 1
        self.startpage = startpage
        self.spidernum = spidernum

    # 爬取总共的页数
    def SpiderPageNum(self):
        url = 'https://fofa.so/result?q={}&qbase64={}&full=true'.format(self.q, self.qbase64)
        html = requests.get(url=url, headers=self.header).text
        pages = re.findall('>(\d*)</a> <a class="next_page" rel="next"', html)
        if len(pages) == 0:
            self.page = 1
        else:
            self.page = pages[0]

    def SpiderPage(self,page,name):
        target = 'https://fofa.so/result?page={}&q={}&qbase64={}&full=true'.format(page, self.q, self.qbase64)
        res = requests.get(url=target, headers=self.header).text
        selector = etree.HTML(res)

        domain1 = selector.xpath('//*[@id="ajax_content"]/div/div/div/a/text()')  # 爬取域名或ip
        domain2 = selector.xpath('//*[@id="ajax_content"]/div/div/div[1]/div[1]/text()')

        domainx = [value.strip(' ').strip('\n').strip(' ') for value in domain1 if len(value) != 0]  # 判断是否为空
        domainy = [value.strip(' ').strip('\n').strip(' ') for value in domain2 if len(value) != 0]  # 判断是否为空

        if len(domainx) == 0:
            domain = domainy
            for value in domain:
                print(value)
                with open('{}.txt'.format(name),'a+') as file:
                    file.writelines(value)
                    file.write('\n')
            time.sleep(random.randint(5, 8))

        if len(domainy) == 0:
            domain = domainx
            for value in domain:
                print(value)
                with open('{}.txt'.format(name), 'a+') as file:
                    file.writelines(value)
                    file.write('\n')
            time.sleep(random.randint(5, 8))

        if len(domainx) != 0 and len(domainy) != 0:
            domainx.extend(domainy)
            for value in domain1:
                print(value)
                with open('{}.txt'.format(name),'a+') as file:
                    file.writelines(value)
                    file.write('\n')
            time.sleep(random.randint(5, 8))


    def SpiderStart(self):
        name = str(time.time()).split('.')[0]
        pagenum = int(self.page) + 1
        try:
            for page in range(self.startpage,pagenum):
                if self.spidernum != 0 and (page == (self.startpage + self.spidernum +1)):
                    break
                print('\033[31m第{}页\033[0m'.format(page))
                self.SpiderPage(page,name)
            sys.stdout.write('\033[31m搜集结果为{}.txt\n\n\033[0m'.format(name))
        except Exception as e:
            print("'\033[31m[!]异常退出！\033[0m'")
            print(e)


    def run(self):

        self.SpiderPageNum()
        self.SpiderStart()


if __name__ == '__main__':
    banner()
    options, args = cmd()
    cookie = "".join(args)

    try:
        if options.source is not None:
            with open(options.source,'r+',encoding='utf-8') as file:
                for value in file.readlines():
                    value = value.strip('\n')
                    spider = FofaSpider(cookie, value, options.startpage, options.spidernum)
                    spider.run()
        else:
            spider = FofaSpider(cookie,options.query,options.startpage, options.spidernum)
            spider.run()

    except Exception as e:
        print("'\033[31m[!]异常退出！\033[0m'")
        print(e)

