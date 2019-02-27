"""新浪新闻"""
import re
import json
import asyncio
import aiohttp
import requests

class Sina_Comment:
    def __init__(self,url):
        self.url = url
        self.cmnt_list = []
        self.hot_list = []
        self.headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'
}

    async def geturl(self,i,u):
        channels = ['jc', 'gn', 'gj', 'cj', 'kj', 'ty', 'yl', 'qc', 'yx', 'shuo', 'qz', 'wj', 'gy', 'fo', 'tousu', 'sf',
                    'sh','pl']
        url = u
        # url = 'https://finance.sina.com.cn/roll/2018-11-07/doc-ihmutuea7787670.shtml'
        p1 = re.compile(r'-i(.*?).shtml', re.S)
        cuturl = re.findall(p1, url)
        for c in channels:  # 遍历正确的js页
            pageurl = 'http://comment5.news.sina.com.cn/page/info?version=1&format=js&channel={0}&newsid=comos-{1}&group=&compress=0&ie=gbk&oe=gbk&page={2}&page_size=20&jsvar=loader_1541659646912_32229203'.format(
                c, cuturl[0], i)
            async with aiohttp.ClientSession() as session:
                async with session.get(pageurl, headers=self.headers) as html:
                    response = await html.text(encoding="utf-8")
                    if len(response) > 1000:
                        return response

    async def parse(self,page,u):
        response = await self.geturl(page,u)
        p2 = re.compile(r'=(.*)', re.S)
        cutjson = re.findall(p2, response)
        respjson = cutjson[0]
        html = json.loads(respjson)
        cmnt_items = html['result']['cmntlist']  # 最新评论
        hot_items = html['result']['hot_list']  # 最热评论
        for cmnt in cmnt_items:
            Mid = cmnt['mid']    #ID
            Name = cmnt['nick']  # 名称
            Area = cmnt['area']  # 位置
            Time = cmnt['time']  # 评论时间
            Content = cmnt['content']  #评论内容
            Newsid = cmnt['newsid']     #Newsid
            Agree = cmnt['agree']       #点赞数
            self.cmnt_list.append({'Mid':Mid,'Newsid':Newsid,'Name': Name, 'Area': Area, 'Content':Content, 'Agree':Agree,'Time': Time})
        for hot in hot_items:
            Mid = hot['mid']     #ID
            Name = hot['nick']  # 名称
            Area = hot['area']  # 位置
            Time = hot['time']  # 评论时间
            Content = hot['content']  # 评论内容
            Newsid = hot['newsid']  # Newsid
            Agree = hot['agree']  # 点赞数
            if len(self.hot_list) < 3:
                self.hot_list.append({'Mid':Mid,'Newsid':Newsid,'Name': Name, 'Area': Area, 'Content':Content, 'Agree':Agree, 'Time': Time})
            else:
                break
    def get_pages(self):
        channels = ['jc', 'gn', 'gj', 'cj', 'kj', 'ty', 'yl', 'qc', 'yx', 'shuo', 'qz', 'wj', 'gy', 'fo', 'tousu', 'sf',
                    'sh', 'pl']
        # url = 'https://finance.sina.com.cn/roll/2018-11-07/doc-ihmutuea7787670.shtml'
        p1 = re.compile(r'-i(.*?).shtml', re.S)
        cuturl = re.findall(p1, self.url)
        for c in channels:  # 遍历正确的js页
            pageurl = 'http://comment5.news.sina.com.cn/page/info?version=1&format=js&channel={0}&newsid=comos-{1}&group=&compress=0&ie=gbk&oe=gbk&page={2}&page_size=20&jsvar=loader_1541659646912_32229203'.format(
                c, cuturl[0], 1)
            response = requests.get(pageurl,headers=self.headers).text
            if len(response) > 1000:
                p4 = re.compile(r'=(.*)', re.S)
                cutjson = re.findall(p4, response)
                respjson = cutjson[0]
                html = json.loads(respjson)
                pages = html['result']['count']['show']
                return pages
    def main(self):
        htmlpages = self.get_pages()
        asyncio.set_event_loop(asyncio.new_event_loop())
        loop = asyncio.get_event_loop()
        tasks = [self.parse(i,self.url) for i in range(1, int(htmlpages/20)+2)]
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()
        sina_commment_dict = {'最新评论': self.cmnt_list, '最热评论': self.hot_list,'type':'xinlang'}
        return sina_commment_dict