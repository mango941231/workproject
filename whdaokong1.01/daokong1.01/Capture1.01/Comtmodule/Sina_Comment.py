"""新浪新闻 2018/12/19 改动：重构了获取最热评论的方式更加准确 减少了错误率"""
import re
import json
import time
import requests
from Capmodule.Capture_XL_Hot import Cap_xlhotnews as xl

class Sina_Comment:
    def __init__(self,url,id,ti):
        self.url = url
        self.Id = id
        self.taskid = ti
        self.hot_list = []
        self.count = 0
        self.channel = ''
        self.cuturl = ''
        self.title = ''
        self.articletime = ''
        self.agree = ''
        self.headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'
}

    def geturl(self):
        channels = ['jc', 'gn', 'gj', 'cj', 'kj', 'ty', 'yl', 'qc', 'yx', 'shuo', 'qz', 'wj', 'gy', 'fo', 'tousu', 'sf',
                    'sh','pl']
        # url = 'https://finance.sina.com.cn/roll/2018-11-07/doc-ihmutuea7787670.shtml'
        p1 = re.compile(r'-i(.*?).shtml', re.S)
        cuturl = re.findall(p1, self.url)
        for c in channels:  # 遍历正确的js页
            pageurl = 'http://comment5.news.sina.com.cn/page/info?format=json&channel={}&newsid=comos-{}'.format(
                c, cuturl[0])
            response = requests.get(pageurl).text
            if len(response) > 1000:
                self.channel = c
                self.cuturl = cuturl[0]
                html = json.loads(response)
                self.title = html['result']['news']['title']
                self.articletime = html['result']['news']['time']
                hot_items = html['result']['hot_list']  # 最热评论
                for hot in hot_items:
                    Mid = hot['mid']  # ID
                    if self.Id == Mid:
                        self.agree = hot['agree']
                    if len(self.hot_list) < 3:
                        self.hot_list.append(Mid)
                    else:
                        break
    def main(self):
        self.geturl()
        pageurl = 'http://comment5.news.sina.com.cn/comment/skin/default.html?channel={0}&newsid=comos-{1}'.format(self.channel,self.cuturl)
        if self.Id in self.hot_list:
            print('%s已更新至热评，正在截图' % self.taskid)
            src = xl(pageurl, self.Id, self.taskid, self.hot_list, self.title, self.articletime, self.agree).capture()
            return src
        else:
            self.count += 1
            print('%s已监控%d次' % (self.taskid, self.count))
            time.sleep(60)
            self.main()