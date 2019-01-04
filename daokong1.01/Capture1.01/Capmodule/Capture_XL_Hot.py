"""新浪热评截图 2018/12/19 改动：(1)重新构造了链接 不用通过点击进入评论页 减少错误率 (2)增加单条热评定位边框"""
from selenium import webdriver
import time
from PIL import Image
import base64
import cv2

class Cap_xlhotnews:
    def __init__(self, url, id, ti, hotlist, title, articletime, agree):
        self.url = url
        self.Id = id
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
        driver.save_screenshot('F:\\picture\\xinlang\\xinlang.png')  #屏幕截图
        elementhot = driver.find_element_by_class_name('hot-wrap')
        xPiont = elementhot.location['x']
        yPiont = elementhot.location['y']
        element_width = elementhot.size['width'] + xPiont
        element_height = yPiont + elementhot.size['height']
        picture = Image.open('F:\\picture\\xinlang\\xinlang.png')
        pic = picture.crop((xPiont, yPiont, element_width, element_height+150))
        pic.save(r'F:\\picture\\xinlang\\xinlang.png')
        element = driver.find_element_by_css_selector(
            '#bottom_sina_comment > div.sina-comment-list.sina-comment-list-has-all.sina-comment-list-has-hot.sina-comment-list-has-latest > div.hot-wrap > div.list > div.clearfix:nth-child({})'.format(
                int(self.hot_list.index(self.Id)) + 1))
        xPiont = element.location['x']
        yPiont = element.location['y']
        element_width = xPiont + element.size['width']
        element_height = yPiont + element.size['height']
        elementup = driver.find_element_by_css_selector(
            '#bottom_sina_comment > div.sina-comment-list.sina-comment-list-has-all.sina-comment-list-has-hot.sina-comment-list-has-latest > div.hot-wrap > div.title')
        yPiontup = elementup.location['y']
        image = 'F:\\picture\\xinlang\\xinlang.png'
        img = cv2.imread(image)
        cv2.rectangle(img, (3, yPiont - yPiontup), (elementhot.size['width'] - 5, element_height - yPiontup), (0, 255, 0),
                      5)
        cv2.imwrite(image, img)
        image = 'F:\\picture\\xinlang\\xinlang.png'  #获取图片的二进制字符串
        with open(image, 'rb') as f:
            strb = base64.b64encode(f.read())
        place = int(self.hot_list.index(self.Id)) + 1
        datadict = {'type': '1', 'taskid': self.taskid, 'title': self.title, 'newtime': self.articletime,
                    'zannumber': self.agree, 'weizhi': str(place), 'url': str(strb, encoding="utf-8")}
        apiurl = 'http://127.0.0.1:888/Port/getpic.php'
        requests.post(apiurl,data=datadict)
        print('已请求接口')
        return datadict