"""凤凰新闻"""
import re
import json
import time
import requests
from urllib import parse
from Capmodule.Capture_FH_Hot import Cap_fhhotnews as cf

class Fh_Comment:
    def __init__(self,url,id,ti):
        self.url = url
        self.taskid = ti
        self.Id = id
        self.cmnt_list = []
        self.hot_list = []
        self.count = 0
        self.docurl = self.url
        self.title = ''
        self.articletime = ''
        self.agree = ''
        params = {
            'callback': 'newCommentListCallBack',
            'orderby': '',
            'docUrl': self.url,
            'format': 'js',
            'job': 1,
            'p': 1,
            'pageSize': 20,
            'callback': 'newCommentListCallBack',
            'skey': '38eaaf'
        }
        data = parse.urlencode(params)
        pageurl = 'https://comment.ifeng.com/get.php?{}'.format(data)
        response = requests.get(pageurl).text
        p1 = re.compile(r'=(.*?)};', re.S)
        cuturl = re.findall(p1, response)
        commentjson = cuturl[0] + "}"
        html = json.loads(commentjson)
        '''处理多种链接不同的情况 比如财经、娱乐等栏目和资讯链接不同'''
        if html['comments'] == []:
            resp = requests.get(url).text
            p2 = re.compile(r'"commentUrl":"(.*?)",', re.S)
            cut = re.findall(p2, resp)
            self.docurl = cut[0]
    def get_hot(self):
        parms = {
            'callback': 'hotCommentListCallBack',
            'orderby': 'uptimes',
            'docUrl': self.docurl,
            'format': 'js',
            'job': 1,
            'p': 1,
            'pageSize': 10,
            'callback': 'hotCommentListCallBack',
            'skey': '38eaaf'
        }
        data = parse.urlencode(parms)
        pageurl = 'https://comment.ifeng.com/get.php?{}'.format(data)
        response = requests.get(pageurl).text
        p1 = re.compile(r'=(.*?)};', re.S)
        cuturl = re.findall(p1, response)
        commentjson = cuturl[0] + "}"
        html = json.loads(commentjson)
        hotcomments = html['comments']
        for hot in hotcomments:
            CmtID = hot['comment_id']  # 评论ID
            self.title = hot['doc_name']       #文章标题
            self.articletime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(int(hot['add_time'])))   #文章发布时间
            if hot['comment_id'] == self.Id:
                self.agree = str(hot['uptimes'])    #点赞数
            self.hot_list.append(CmtID)

    def main(self):
        self.get_hot()
        resp = requests.get(url=self.url).text
        p4 = re.compile(r'<title>(.*?)_.*?</title>', re.S)
        docname = re.findall(p4, resp)
        p3 = re.compile(r'"commentUrl":"(.*?)",', re.S)
        docurl = re.findall(p3, resp)
        if docurl == []:
            p3 = re.compile(r'"commentUrl": "(.*?)",', re.S)
            docurl = re.findall(p3, resp)
        nextparams = {
            'docUrl':docurl[0],
            'docName':docname[0],
            'skey': '38eaaf',
            'pcUrl':self.url
        }
        data = parse.urlencode(nextparams)
        nexturl = 'http://gentie.ifeng.com/view.html?{}'.format(data)

        if self.Id in self.hot_list:
            print('%s已更新至热评，正在截图' % self.taskid)
            src = cf(nexturl, self.Id, self.taskid, self.hot_list, self.title, self.articletime, self.agree).capture()
            return src
        else:
            self.count += 1
            print('%s已监控%d次' % (self.taskid, self.count))
            time.sleep(60)
            self.main()