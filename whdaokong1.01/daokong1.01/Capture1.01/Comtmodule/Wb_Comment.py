"""新浪微博"""
import re
import json
import time
import requests
from pyquery import PyQuery as pq
from Capmodule.Capture_WB_Hot import Cap_wbhotnews as cw

class Wb_Comment:
    def __init__(self,url,id,ti):
        self.hot_list = []
        self.Id = id
        self.url = url
        self.taskid = ti
        self.count = 0
        self.title = ''
        self.articletime = ''
        self.agree = ''
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
            'Cookie': 'M_WEIBOCN_PARAMS=uicode%3D20000174;MLOGIN=1;SUB=_2A252-zFfDeRhGeBK4lAX8i7LzjuIHXVSBF8XrDV6PUJbkdANLU7ikW1NRx7V61MobIwfOf6j2OC4-fKJYW8DCEy-;SCF=Ak419-qJJKRPEN_WvFSQFOXJu9s1zrQ5LAMMZx7N2hdcNMuC2KOTb8GkaQnLAt84Rn9UgBW88qdC__4JkqSIhZI.;SUHB=0S7CImebougT2s;SSOLoginState=1543454991;WEIBOCN_FROM=1110006030;_T_WM=20cd9b394e948f272b8c0e90aaaab33e'
        }
        resp = requests.get(url, headers=self.headers).text
        p1 = re.compile(r'rid=(.*?)&', re.S)
        cut = re.findall(p1, resp)
        self.mid = cut[0]
        # self.pageurl = 'https://weibo.com/aj/v6/comment/big?ajwvr=6&id={}&filter=all&page=1'.format(self.mid)
        self.pageurl = 'https://weibo.com/aj/v6/comment/big?id={}&from=singleWeiBo&__rnd=1545206992544'.format(self.mid)
    def get_frist(self):
        response = requests.get(self.pageurl, headers=self.headers).text
        htmljson = json.loads(response)
        html = htmljson['data']['html']  # 获取网页的代码元素
        doc = pq(html)
        items = doc('div.list_box > div.list_ul > div').items()
        for item in items:
            ID = item.attr('comment_id')  # ID
            if self.Id == ID:
                self.agree = item('div.list_con > div.WB_func.clearfix > div.WB_handle.W_fr > ul > li:nth-child(4) > span > a > span > em:nth-child(2)').text()
                if self.agree == '赞':
                    self.agree = 0
            self.hot_list.append(ID)
    def get_info(self):
        resp = requests.get(self.url,headers=self.headers).text
        p1 = re.compile(r'.*<meta content="(.*?)" name="description" />', re.S)
        cuttitle = re.findall(p1, resp)
        self.title = cuttitle[0]    #个人微博正文
        mat = re.search(r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})", resp)
        self.articletime = mat.group(0)     #微博发布时间
    def main(self):
        self.get_frist()
        self.get_info()
        time.sleep(5)
        if len(self.hot_list) > 10:
            if self.Id in self.hot_list[0:10]:
                print('%s已更新至热评，正在截图' % self.taskid)
                src = cw(self.url, self.Id, self.taskid, self.hot_list, self.title, self.articletime, self.agree).capture()
                return src
            else:
                self.count += 1
                print('%s已监控%d次' % (self.taskid, self.count))
                time.sleep(60)
                self.main()
        else:
            if self.Id in self.hot_list:
                print('%s已更新至热评，正在截图' % self.taskid)
                src = cw(self.url, self.Id, self.taskid, self.hot_list, self.title, self.articletime, self.agree).capture()
                return src
            else:
                self.count += 1
                print('%s已监控%d次' % (self.taskid, self.count))
                time.sleep(60)
                self.main()