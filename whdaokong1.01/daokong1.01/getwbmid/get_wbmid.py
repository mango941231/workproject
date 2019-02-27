import requests
import useragent as ug
import random
import re
import os
class Get_Wbmid:
    def __init__(self,url):
        self.url = url
        f = open('xinlang.txt', 'r')
        lines = f.readlines()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
            'Cookie': re.sub('[\n]', '', random.choice(lines))
        }
    def main(self):
        resp = requests.get(self.url, headers=self.headers).text
        p1 = re.compile(r'mblogid=(.*?)&', re.S)
        cut = re.findall(p1, resp)
        mid = {'Mid':cut[0]}
        return mid
