"""搜狐新闻"""
import json
import time
import requests
import re
from urllib import parse
from pyquery import PyQuery as pq
from Capmodule.Capture_SH_Hot import Cap_shhotnews as sh

class Sh_Comment:
    def __init__(self,url,id,ti):
        self.taskid = ti
        self.url = url
        self.Id = id
        self.count = 0
        resp = requests.get(self.url).text
        doc = pq(resp)
        self.topic_title = doc('.wrapper-box .text-title h1').text()  # 文章标题
        p = re.compile(r'.*/(.*?)_.*', re.S)
        cut = re.findall(p, self.url)
        self.source_id = 'mp_' + cut[0]                 # source_id
        self.hot_list = []
        self.title = self.topic_title       #文章标题
        self.articletime = doc('#news-time').text()    #文章发布时间
        self.agree = ''

    def hot_comment(self):
        params = {
            'callback':'jQuery1124039668336202851107_1542852755754',
            'page_size':10,
            'topic_source_id':556070408,
            'page_no':1,
            'hot_size':5,
            'media_id':255783,
            'topic_category_id':8,
            'topic_title':self.topic_title,
            'topic_url':self.url,
            'source_id':self.source_id,
            '_':1542852755787
        }
        data = parse.urlencode(params)
        pageurl = 'http://apiv2.sohu.com/api/topic/load?{}'.format(data)
        response = requests.get(pageurl).text
        p1 = re.compile(r'[(](.*)[)]', re.S)
        pagejson = re.findall(p1,response)
        html = json.loads(pagejson[0])
        hots = html['jsonObject']['hots']
        for hot in hots:
            Comment_id = str(hot['comment_id'])
            if self.Id == Comment_id:
                self.agree = hot['support_count']   #点赞数
            self.hot_list.append(Comment_id)
    def main(self):
        self.hot_comment()
        if self.Id in self.hot_list:
            print('%s已更新至热评，正在截图' % self.taskid)
            src = sh(self.url, self.Id, self.taskid, self.hot_list, self.title, self.articletime, self.agree).capture()
            return src
        else:
            self.count += 1
            print('%s已监控%d次' %(self.taskid, self.count))
            time.sleep(60)
            self.main()