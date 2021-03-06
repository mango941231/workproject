"""网易新闻 2018/12/18 改动：热评准确抓取 并且 顺序一致"""
import requests
import re
import json
import asyncio
import aiohttp
import uvloop
from urllib import parse
from collections import OrderedDict

class Wy_Comment:
    def __init__(self,url):
        self.url = url
        self.hot_list = []
        self.new_list = []
        '''处理军事链接不同'''
        if 'photoview' in self.url:
            resp = requests.get(self.url).text
            p1 = re.compile(r'"docId" :  "(.*?)",', re.S)
            self.cuturl = re.findall(p1, resp)
        else:
            p3 = re.compile(r'.*/(.*).html', re.S)
            self.cuturl = re.findall(p3, self.url)  # 正则匹配出文章链接内特定的参数
        self.hocom_list = []
        self.hot_id = []

    def get_hot(self):
        t1 = [5, 35]
        t2 = [0, 5]
        for li,ft in zip(t1,t2):
            params = {
                'ibc':'newspc',
                'limit':li,
                'showLevelThreshold':72,
                'headLimit':1,
                'tailLimit':2,
                'offset':ft,
                'callback':'jsonp_1542251915219',
                '_':1542251915220
            }
            data = parse.urlencode(params)
            page_url = 'http://comment.api.163.com/api/v1/products/a2869674571f77b5a0867c3d71db5856/threads/{0}/comments/hotList?{1}'.format(self.cuturl[0],data)
            response = requests.get(page_url).text
            p2 = re.compile(r'[(]\n(.*)[)]', re.S)
            cut_json = re.findall(p2, response)
            page_json = cut_json[0]
            html = json.loads(page_json)
            hot_comments = list(html['commentIds'])
            for i in hot_comments:
                if ',' in i:
                    p3 = re.compile(r'.*,(.*)', re.S)
                    cuti = re.findall(p3, i)
                    xiabiao = hot_comments.index(i)
                    hot_comments[xiabiao] = cuti[0]
            comments = html['comments']
            for hotid in hot_comments:
                htmlid = comments[hotid]
                CommentId = htmlid['commentId']  # 评论ID
                Area = htmlid['user']['location']  # 地区
                if 'nickname' in htmlid['user']:  # 评论用户名
                    Name = htmlid['user']['nickname']
                else:
                    Name = '网易' + Area + '网友'
                Content = htmlid['content']  # 评论内容
                Time = htmlid['createTime']  # 评论时间
                ProductKey = htmlid['productKey']
                Agree = htmlid['vote']
                self.hot_list.append({'CommentId':str(CommentId),'Name': Name, 'Area': Area,'Content':Content,'Agree':str(Agree),'Time':Time,'ProductKey':ProductKey,'PostId':self.cuturl[0]})
        for i in reversed(range(len(self.hot_list))):
            if self.hot_list[i].get('Content') == '跟贴被火星网友带走啦~':
                self.hot_list.pop(i)

    async def getnews(self,page):
        params = {
            'ibc': 'newspc',
            'limit': 30,
            'showLevelThreshold': 72,
            'headLimit': 1,
            'tailLimit': 2,
            'offset': page,
            'callback': 'jsonp_1542251915219',
            '_': 1542251915220
        }
        data = parse.urlencode(params)
        pageurl = 'http://comment.api.163.com/api/v1/products/a2869674571f77b5a0867c3d71db5856/threads/{0}/comments/newList?{1}'.format(
            self.cuturl[0], data)
        async with aiohttp.ClientSession() as session:
            async with session.get(pageurl) as pagehtml:
                response = await pagehtml.text(encoding="utf-8")
                p2 = re.compile(r'[(]\n(.*)[)]', re.S)
                cutjson = re.findall(p2, response)
                pagejson = cutjson[0]
                html = json.loads(pagejson)
                newcomments = html['comments']
                newhtml = dict(newcomments)
                for new in newhtml.values():
                    CommentId = new['commentId']  # 评论ID
                    Area = new['user']['location']  # 地区
                    if 'nickname' in new['user']:  # 评论用户名
                        Name = new['user']['nickname']
                    else:
                        Name = '网易' + Area + '网友'
                    Content = new['content']  # 评论内容
                    Time = new['createTime']  # 评论时间
                    ProductKey = new['productKey']
                    Agree = new['vote']
                    self.new_list.append({'CommentId':str(CommentId),'Name': Name, 'Area': Area,'Content':Content,'Agree':str(Agree),'Time':Time,'ProductKey':ProductKey,'PostId':self.cuturl[0]})

    def main(self):
        self.get_hot()
        url = f'http://comment.api.163.com/api/v1/products/a2869674571f77b5a0867c3d71db5856/threads/{self.cuturl[0]}/comments/newList?limit=30&offset=0'
        respjson = requests.get(url).json()
        page = int(respjson['newListSize'] / 30) + 1
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        loop = uvloop.new_event_loop()
        asyncio.set_event_loop(loop)
        # asyncio.set_event_loop(asyncio.new_event_loop())
        # loop = asyncio.get_event_loop()
        tasks = [self.getnews(i*30) for i in range(page)]
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()
        b = OrderedDict()
        for item in self.new_list:
            b.setdefault(item['CommentId'], {**item, })
        self.new_list = list(b.values())
        for i in reversed(range(len(self.new_list))):
            if self.new_list[i].get('Content') == '跟贴被火星网友带走啦~':
                self.new_list.pop(i)
        wy_commment_dict = {'最新评论': self.new_list, '最热评论': self.hot_list,'type':'wangyi'}
        # wy_commment_dict = {'最新评论': len(self.new_list), '最热评论': len(self.hot_list)}
        # print(wy_commment_dict)
        return wy_commment_dict