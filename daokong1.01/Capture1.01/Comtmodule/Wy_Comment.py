"""网易新闻 2018/12/18 改动：热评准确抓取 并且 顺序一致"""
import re
import json
import time
import requests
from urllib import parse
from collections import OrderedDict
from Capmodule.Cap_WY_Hot import Cap_wyhotnews as wy

class Wy_Comment:
    def __init__(self,url,id,ti):
        self.url = url
        self.taskid = ti
        self.Id = id
        self.count = 0
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
        self.hotlist = []
        self.hotlistid = []
        self.title = ''
        self.articletime = ''
        self.agree = ''

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
                commentId = htmlid['commentId']
                if self.Id == str(commentId):
                    self.agree = htmlid['vote']
                # Content = htmlid['content']
                self.hot_list.append(str(commentId))
        # for i in reversed(range(len(self.hot_list))):
        #     if self.hot_list[i].get('Content') == '跟贴被火星网友带走啦~':
        #         self.hot_list.pop(i)
    def get_info(self):
        url = 'http://comment.api.163.com/api/v1/products/a2869674571f77b5a0867c3d71db5856/threads/{0}'.format(self.cuturl[0])
        resp = requests.get(url).text
        respjson = json.loads(resp)
        self.title = respjson['title']
        self.articletime = respjson['createTime']
    def main(self):
        self.get_hot()
        self.get_info()
        if self.Id in self.hot_list:
            print('已更新至热评，正在截图')
            src = wy(self.url, self.hot_list, self.taskid, self.Id, self.title, self.articletime, self.agree).capture()
            return src
        else:
            self.count += 1
            print('已监控%d次' % self.count)
            time.sleep(60)
            self.main()