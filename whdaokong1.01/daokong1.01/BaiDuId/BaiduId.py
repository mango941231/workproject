import requests
from pyquery import PyQuery as pq
import difflib
import re
class BaiduId:
    def __init__(self, keywords, title, url):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
        }
        self.keywords = keywords
        self.title = title
        self.url = url
        self.id = ''
    def get_id(self):
        try:
            for i in range(0, 20, 10):
                url = f'https://www.baidu.com/s?wd={self.keywords}&pn={i}'
                response = requests.get(url, headers=self.headers).text
                html = pq(response)
                items = html('#content_left .result.c-container ').items()
                print(i)
                for item in items:
                    htmlurl = item.find('div.f13 > a.c-showurl').text()
                    if '...' in htmlurl:
                        htmlurl = htmlurl.replace('...', '')
                    htmltitle = item.find('.t').text()
                    similarity = difflib.SequenceMatcher(None, self.title, htmltitle).quick_ratio()
                    if similarity > 0.90 and htmlurl in self.url:
                        id = item.find('.f13 .c-tools').attr('id')
                        p1 = re.compile(r'(.*)_', re.S)
                        cut = re.findall(p1, id)
                        self.id = cut[0]
                        print('页面链接%s   页面标题%s' % (htmlurl, htmltitle))
                        break
                if self.id != '':
                    print('%s位于第%d页' % (self.id, i/10+2))
                    break
            # data = {'id': str(self.id)}
            return self.id
        except BaseException as e:
            # data = {'id': e}
            return e



