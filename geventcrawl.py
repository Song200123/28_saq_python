from _typeshed import Self
from threading import main_thread
from gevent.hub import MAIN_THREAD_IDENT
import requests
from queue import Queue
from bs4 import BeautifulSoup
import re
import time
import gevent

class Spider:
    def __init__(self):
        self.headers ={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'}
        #基准网址
        self.base_url = 'https://fanqienovel.com/rank/xianyan/page_()'
        #数据队列
        self.dataQueue = Queue()
        #统计数量
        #self.count = 0
        #数据列表
        self.novels = []

    #获取一页数据的方法
    def get_page_url(self, url):
        content = requests.get(url, headers=self.headers).content

        #d对页面数据进行解析
        soup = BeautifulSoup(content,'html5lib')#将解析的文档放在soup变量里

        novels_list = soup.find('div',class_='muye-rank')#找到那个小说所在的div
        pattern = re.complie() 
        novellist_box = novels_list.find_all('div',class_='pattern')

        novels = []
        for novellist in novellist_box:
            novel = {}
            novel['img'] = novellist.find('div',class_='book-cover loaded').find('img')['src']
            novel['title'] = novellist.find('div',class_='title').find('a').text

        Self.dataQueue.put(novel)

    def start_work(self,pageNum):
        job_list = []
        for page in range(1, pageNum+1):
            url = self.base_url.format(page)
            #创建携程任务
            job = gevent.spawn(self.get_page_novels, url)
            #把所有协程任务加入任务列表
            job_list.append(job)

        #等待所有协程执行完毕
        gevent.joinall(job_list)

        while not self.dataQueue.empty():
            novel = self.dataQueue.get()  #获取数据
            self.novels.append(novel)

if __name__ =="__main__":
    pages = int(input('请输入页码:'))
    t1 = time.time()
    spider = Spider()
    spider.start_work(pages)
    print(len(spider.novels))
    t2 = time.time()
    print(t2 - t1)
