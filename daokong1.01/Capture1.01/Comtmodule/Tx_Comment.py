"""腾讯新闻"""
import re
import json
import time
import requests
from urllib import parse
from Capmodule.Capture_TX_Hot import Cap_txhotnews as ct
class Tx_Comment:
    def __init__(self, url, id, ti):
        self.url = url
        self.taskid = ti
        self.Id = id
        self.hot_list = []
        self.count = 0
        self.agree = ''
        self.title = ''
        self.articletime = ''
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'
        }
        '''分析多种不同的腾讯新闻链接'''
        try:
            if 'news' in self.url:
                html = requests.get(self.url,headers=self.headers).text
                p1 = re.compile(r'cmt_id = (.*?);', re.S)
                cutjson = re.findall(p1, html)
                self.comid = cutjson[0]
                p2 = re.compile(r"pubtime:'(.*)'", re.S)
                cutpubtime = re.findall(p2, html)
                self.articletime = cutpubtime[0]    #文章发布时间
                p3 = re.compile(r"title:'(.*)'", re.S)
                cuttitle = re.findall(p3, html)
                self.title = cuttitle[0]        #文章标题
            elif len(self.url.split('/')) == 5:
                p1 = re.compile(r'.*/(.*)', re.S)
                cutpara = re.findall(p1, self.url)
                param = {
                    'id': cutpara[0],
                    'chlid': 'news_rss',
                    'refer': 'mobilewwwqqcom',
                    'otype': 'jsonp',
                    'ext_data': 'all',
                    'srcfrom': 'newsapp',
                    'callback': 'getNewsContentOnlyOutput'
                }
                # https: // openapi.inews.qq.com / getQQNewsNormalContent?id = NEW2018112201551000 & chlid = news_rss & refer = mobilewwwqqcom & otype = jsonp & ext_data = all & srcfrom = newsapp & callback = getNewsContentOnlyOutput
                paradata = parse.urlencode(param)
                paraurl = 'https://openapi.inews.qq.com/getQQNewsNormalContent?{}'.format(paradata)
                html = requests.get(paraurl,headers=self.headers).text
                p2 = re.compile(r'[(](.*)[)]', re.S)
                cutparajson = re.findall(p2, html)
                parajson = json.loads(cutparajson[0])
                self.comid = parajson['cid']
                timeurl = 'https://openapi.inews.qq.com/getQQNewsNormalContent?id={}&refer=mobilewwwqqcom&ext_data=all'.format(cutpara[0])
                timeresp = requests.get(timeurl,headers=self.headers).text
                # p4 = re.compile(r'[(](.*)[)]', re.S)
                # cuttimejson = re.findall(p4, timeresp)
                timejson = json.loads(timeresp)
                self.title = timejson['title']      #文章标题
                self.articletime = timejson['pubtime']  #文章发布时间
            else:
                html = requests.get(self.url).text
                p1 = re.compile(r'window.DATA = (.*?)}', re.S)
                cutjson = re.findall(p1, html)
                if cutjson:
                    p2 = re.sub('[\t\n]', '', cutjson[0])
                    p3 = p2 + '}'
                    p4 = json.loads(p3)
                    self.comid = p4['comment_id']
                    self.title = p4['title']
                    self.articletime = p4['pubtime']
                else:
                    p5 = re.compile(r'.*/(.*)', re.S)
                    cutpara = re.findall(p5, self.url)
                    param = {
                        'id': cutpara[0],
                        'chlid': 'news_rss',
                        'refer': 'mobilewwwqqcom',
                        'otype': 'jsonp',
                        'ext_data': 'all',
                        'srcfrom': 'newsapp',
                        'callback': 'getNewsContentOnlyOutput'
                    }
                    # https: // openapi.inews.qq.com / getQQNewsNormalContent?id = NEW2018112201551000 & chlid = news_rss & refer = mobilewwwqqcom & otype = jsonp & ext_data = all & srcfrom = newsapp & callback = getNewsContentOnlyOutput
                    paradata = parse.urlencode(param)
                    paraurl = 'https://openapi.inews.qq.com/getQQNewsNormalContent?{}'.format(paradata)
                    html = requests.get(paraurl,headers=self.headers).text
                    p2 = re.compile(r'[(](.*)[)]', re.S)
                    cutparajson = re.findall(p2, html)
                    parajson = json.loads(cutparajson[0])
                    self.comid = parajson['cid']
        except Exception:
            print('链接格式错误')

    def get_hot(self):
        params = {
            'callback': '_article{}commentv2'.format(self.comid),
            'orinum': 10,
            'oriorder': 'o',
            'pageflag': 1,
            'cursor': 0,
            'scorecursor': 0,
            'orirepnum': 2,
            'reporder': 'o',
            'reppageflag': 1,
            'source': 1,
            '_': 1542339702912
        }
        data = parse.urlencode(params)
        page_url = 'http://coral.qq.com/article/{}/comment/v2?{}'.format(self.comid, data)
        response = requests.get(page_url,headers=self.headers).text
        p5 = re.compile(r'[(](.*)[)]', re.S)
        hot_json = re.findall(p5, response)
        page_json = hot_json[0]
        hot_html = json.loads(page_json)
        hot_comments = hot_html['data']['oriCommList']
        for hot in hot_comments:
            ID = hot['id']
            if self.Id == ID:
                self.agree = hot['up']
            self.hot_list.append(ID)
    def main(self):
        self.get_hot()
        pageurl = 'http://coral.qq.com/{}'.format(self.comid)
        if self.Id in self.hot_list:
            print('%s已更新至热评，正在截图' % self.taskid)
            src = ct(pageurl, self.Id, self.taskid, self.hot_list, self.title, self.articletime, self.agree).capture()
            return src
        else:
            self.count += 1
            print('%s已监控%d次' % (self.taskid, self.count))
            time.sleep(60)
            self.main()