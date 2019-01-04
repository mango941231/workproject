"""新浪微博"""
import requests
import json
from pyquery import PyQuery as pq
import re
import datetime
import asyncio
import aiohttp
import random
import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
import useragent
class Crawl_WB_Commenthtml:
    def __init__(self,url):
        self.cmnt_list = []
        self.headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6',
        'Cookie': 'M_WEIBOCN_PARAMS=uicode%3D20000174;MLOGIN=1;SUB=_2A25xDKuyDeRhGeBL71YV-S_Nyj-IHXVSDjX6rDV6PUJbkdAKLU_HkW1NRxo1x1zfxa-o3f1kf1tQPWGVzFB0ubsz;SCF=ApFxuydWjqvsEzoQa-KGusT0Jr4U7FKep9qqzSbAZJwv_xb2EpC68-lqFAjM-3Fa7PyLaJzZ5G_D3SYafbyfuh4.;SUHB=0XDlMthwQ76fUm;SSOLoginState=1544084450;WEIBOCN_FROM=1110006030;_T_WM=2d85bdfb6030d1b3b748cdcbfa91aa1a'
    }
        resp = requests.get(url, headers=self.headers).text
        p1 = re.compile(r'rid=(.*?)&', re.S)
        cut = re.findall(p1, resp)
        self.mid = cut[0]
        self.url = 'https://weibo.com/aj/v6/comment/big?ajwvr=6&id={}&filter=all&page=1'.format(self.mid)

    async def get_comment(self,i):
        if len(self.cmnt_list) % 5000 == 0 and len(self.cmnt_list) != 0:
            f = open('xinlang.txt', 'r')
            lines = f.readlines()  # 获取本地cookie列表
            self.headers = {
                'User-Agent': random.choice(useragent.agents),
                'Cookie': re.sub('[\n]', '', random.choice(lines))
            }
            print('已更换Cookie、User-agent')

        pageurl = 'https://weibo.com/aj/v6/comment/big?ajwvr=6&id={0}&filter=all&page={1}'.format(self.mid,i)
        async with aiohttp.ClientSession() as session:
            async with session.get(pageurl,headers=self.headers) as pagehtml:
                response = await pagehtml.text("utf-8","ignore")
                htmljson = json.loads(response)
                html = htmljson['data']['html']  # 获取网页的代码元素
                doc = pq(html)
                items = doc('.list_box .list_ul .list_li').items()
                for item in items:
                    Name = item.find('.WB_text a:nth-child(1)').text()  # 名字
                    cont = item.find('.WB_text').text()
                    p1 = re.compile(r'：(.*)', re.S)
                    cuturl = re.findall(p1, cont)
                    Content = cuturl[0]  # 内容
                    Time = item.find('.WB_from').text()  # 时间
                    if '今天' in Time:
                        i = datetime.datetime.now()
                        monthday = str(i.month) + '月' + str(i.day) + '日'
                        Time = re.sub(r'今天', monthday, Time)
                    ID = item.attr('comment_id')  # ID
                    Agree = item.find('.clearfix .S_txt1 span em:nth-child(2)').text()
                    if Agree == '赞':
                        Agree = 0
                    self.cmnt_list.append({'Mid': ID, 'Name': Name, 'Content': Content, 'Time': Time, 'Agree': Agree})
    def get_pages(self):
        response = requests.get(self.url, headers=self.headers).text
        htmljson = json.loads(response)
        pages = htmljson['data']['page']['totalpage']
        return pages

    def main(self):
        try:
            pages = self.get_pages()
            asyncio.set_event_loop(asyncio.new_event_loop())
            loop = asyncio.get_event_loop()
            tasks = [self.get_comment(i) for i in range(1,pages+1)]
            loop.run_until_complete(asyncio.wait(tasks))
            loop.close()
            # wb_comment_dict = {'最新评论': len(self.cmnt_list)}
            wb_comment_dict = {'最新评论': self.cmnt_list,'type': 'weibo'}
            # print(wb_comment_dict)
            return wb_comment_dict
        except BaseException as e:
            print(e)