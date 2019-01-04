"""腾讯新闻热评截图 2018/12/19 增加单条热评定位边框"""
from selenium import webdriver
import time
import base64
import cv2
import requests

class Cap_txhotnews:
    def __init__(self, url, id, ti, hotlist, title, articletime, agree):
        self.url = url
        self.Id = str(id)
        self.taskid = ti
        self.hot_list = list(hotlist)
        self.title = title
        self.articletime = articletime
        self.agree = agree

    def capture(self):
        driver = webdriver.PhantomJS()
        driver.maximize_window()
        driver.get(self.url)
        time.sleep(5)
        driver.save_screenshot('D:\\pythonflask\\jietupicture\\tengxun\\tengxun.png')  # 屏幕截图
        driver.switch_to.frame('commentIframe')     #对于网页里面包含iframe标签元素，使用“driver.switch_to.frame('iframe标签的name或id')”语法进入<iframe>标签里，再进行查找元素。
        """单条评论加上边框"""
        element = driver.find_element_by_css_selector('#J_Comment{}'.format(self.Id))
        xPiont = element.location['x'] + 180
        yPiont = element.location['y'] + 80
        element_width = xPiont + element.size['width']
        element_height = yPiont + element.size['height'] + 40
        image = 'D:\\pythonflask\\jietupicture\\tengxun\\tengxun.png'
        img = cv2.imread(image)
        cv2.rectangle(img, (xPiont, yPiont), (element_width, element_height), (0, 255, 0), 5)
        cv2.imwrite(image, img)
        image = 'D:\\pythonflask\\jietupicture\\tengxun\\tengxun.png'  # 获取图片的二进制字符串
        with open(image, 'rb') as f:
            strb = base64.b64encode(f.read())
        place = int(self.hot_list.index(self.Id)) + 1
        datadict = {'type': '1', 'taskid': self.taskid, 'title': self.title, 'newtime': self.articletime,
                    'zannumber': self.agree, 'weizhi': str(place), 'url': str(strb, encoding="utf-8")}
        apiurl = 'http://127.0.0.1:888/Port/getpic.php'
        requests.post(apiurl,data=datadict)
        print('已请求接口')
        return datadict
