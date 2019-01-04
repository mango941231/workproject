import requests
from pyquery import PyQuery as pq
import difflib
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
            for i in range(0, 200, 10):
                url = f'https://www.baidu.com/s?wd={self.keywords}&pn={i}'
                response = requests.get(url, headers=self.headers).text
                html = pq(response)
                items = html('#content_left .result.c-container ').items()
                for item in items:
                    htmlurl = item.find('.f13 .c-showurl').text()
                    htmltitle = item.find('.t').text()
                    similarity = difflib.SequenceMatcher(None, self.title, htmltitle).quick_ratio()
                    if similarity > 0.80 and htmlurl in self.url:
                        self.id = item.find('.f13 .c-tools').attr('id')
                        break
                if self.id != '':
                    break
            data = {'id': self.id}
            return data
        except BaseException as e:
            data = {'id': e}
            return data



