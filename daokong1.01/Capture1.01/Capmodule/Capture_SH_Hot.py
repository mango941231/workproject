"""搜狐新闻热评截图 2018/12/19 增加单条热评定位边框"""
from selenium import webdriver
import time
import base64
import requests
from PIL import Image
import cv2

class Cap_shhotnews:
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
        driver.get(self.url)
        time.sleep(5)
        driver.find_element_by_class_name('comment-icon').click()
        time.sleep(5)
        driver.save_screenshot('/dkpt_pj/jietupicture/souhu/souhu.png')  # 屏幕截图
        element = driver.find_element_by_css_selector('#mpbox > div.c-comment-content > div > div:nth-child(2)')
        xPiont = element.location['x']
        yPiont = element.location['y']
        element_width = xPiont + element.size['width']
        element_height = yPiont + element.size['height']
        picture = Image.open('/dkpt_pj/jietupicture/souhu/souhu.png')
        pic = picture.crop((xPiont - 10, yPiont-50, element_width + 20, element_height + 70))
        pic.save(r'/dkpt_pj/jietupicture/souhu/souhu.png')
        """单条评论加上边框"""
        element = driver.find_element_by_css_selector(
            '#mpbox > div.c-comment-content > div > div:nth-child(2) > div:nth-child({})'.format(
                int(self.hot_list.index(self.Id)) + 1))
        xPiont = element.location['x']
        yPiont = element.location['y']
        # element_width = xPiont + element.size['width']
        element_height = yPiont + element.size['height']
        elementup = driver.find_element_by_css_selector('#mpbox > div.c-comment-content > div > div.c-comment-title.c-hot')
        yPiontup = elementup.location['y']
        image = '/dkpt_pj/jietupicture/souhu/souhu.png'
        img = cv2.imread(image)
        cv2.rectangle(img, (3, yPiont - yPiontup + 20), (element.size['width'] + 20, element_height - yPiontup + 20), (0, 255, 0),5)
        cv2.imwrite(image, img)
        image = '/dkpt_pj/jietupicture/souhu/souhu.png'  # 获取图片的二进制字符串
        driver.quit()
        with open(image, 'rb') as f:
            strb = base64.b64encode(f.read())
        place = int(self.hot_list.index(self.Id)) + 1
        datadict = {'type': '1', 'taskid': self.taskid, 'title': self.title, 'newtime': self.articletime, 'zannumber': self.agree, 'weizhi': str(place), 'url': str(strb, encoding="utf-8")}
        apiurl = 'http://dk.anming.pro/Port/getpic.php'
        requests.post(apiurl,data=datadict)
        print('已请求接口')
        return datadict
