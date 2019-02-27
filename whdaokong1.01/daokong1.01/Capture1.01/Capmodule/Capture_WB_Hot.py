"""微博新闻热评截图 2018/12/20 增加单条热评定位边框"""
from selenium import webdriver
import time
import base64
from PIL import Image
import cv2
import requests

class Cap_wbhotnews:
    def __init__(self, url, id, ti, hotlist, title, articletime, agree):
        self.url = url
        self.Id = id
        self.taskid = ti
        self.hot_list = list(hotlist)
        self.title = title
        self.articletime = articletime
        self.agree = agree

    def capture(self):
        # cutlist = self.hot_list[0:10]
        driver = webdriver.PhantomJS()
        driver.maximize_window()
        driver.get(self.url)
        time.sleep(5)
        driver.save_screenshot('D:\\pythonflask\\jietupicture\\weibo\\weibo.png')
        element = driver.find_element_by_css_selector('#Pl_Official_WeiboDetail__73 > div > div > div > div.WB_feed_repeat.S_bg1.WB_feed_repeat_v3 > div > div.repeat_list')
        xPiont = element.location['x']
        yPiontup = element.location['y']
        element_width = xPiont + element.size['width']
        element_height = yPiontup + element.size['height']
        picture = Image.open('D:\\pythonflask\\jietupicture\\weibo\\weibo.png')
        pic = picture.crop((xPiont - 10, yPiontup, element_width+10, element_height))
        pic.save(r'D:\\pythonflask\\jietupicture\\weibo\\weibo.png')
        """单条评论加上边框"""
        element = driver.find_element_by_css_selector(
            'div.repeat_list > div:nth-child(2) > div > div > div:nth-child({})'.format(
                int(self.hot_list.index(self.Id)) + 1))
        xPiont = element.location['x']
        yPiont = element.location['y']
        element_width = xPiont + element.size['width']
        # element_height = yPiont + element.size['height']
        # elementup = driver.find_element_by_css_selector('div.repeat_list > div:nth-child(2)')
        # yPiontup = element.location['y']
        image = 'D:\\pythonflask\\jietupicture\\weibo\\weibo.png'
        img = cv2.imread(image)
        cv2.rectangle(img, (3, yPiont-yPiontup), (element_width, yPiont+element.size['height']-yPiontup), (0, 255, 0),
                      5)
        cv2.imwrite(image, img)
        image = 'D:\\pythonflask\\jietupicture\\weibo\\weibo.png'  # 获取图片的二进制字符串
        with open(image, 'rb') as f:
            strb = base64.b64encode(f.read())
        place = int(self.hot_list.index(self.Id)) + 1
        datadict = {'type': '1', 'taskid': self.taskid, 'title': self.title, 'newtime': self.articletime,
                    'zannumber': self.agree, 'weizhi': str(place), 'url': str(strb, encoding="utf-8")}
        apiurl = 'http://127.0.0.1/Port/getpic.php'
        requests.post(apiurl,data=datadict)
        print('已请求接口')
        return datadict
