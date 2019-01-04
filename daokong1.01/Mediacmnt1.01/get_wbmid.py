import requests
import useragent as ug
import random
import re
class Get_Wbmid:
    def __init__(self,url):
        self.url = url
        f = open('xinlang.txt', 'r')
        lines = f.readlines()
        self.headers = {
            'User-Agent': random.choice(ug.agents),
            'Cookie': re.sub('[\n]', '', random.choice(lines))
        }
    def main(self):
        resp = requests.get(self.url, headers=self.headers).text
        p1 = re.compile(r'rid=(.*?)&', re.S)
        cut = re.findall(p1, resp)
        mid = {'Mid':cut[0]}
        return mid
