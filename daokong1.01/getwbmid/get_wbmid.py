import re
from urltomid import *

class Get_Wbmid:
    def __init__(self,url):
        self.url = url
    def main(self):
        '''
        url = 'https://weibo.com/1644114654/HjvFG2VZ1?ref=feedsdk&type=comment#_rnd1551865987128'
        '''
        p1 = re.compile(r'.*/(.*?)[?]', re.S)
        cut = re.findall(p1, self.url)
        mid = url_to_mid(cut[0])
        midr = {'Mid': str(mid)}
        return midr
