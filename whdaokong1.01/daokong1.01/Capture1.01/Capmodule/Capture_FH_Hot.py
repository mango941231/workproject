"""凤凰新闻热评截图 2018/12/19 增加单条热评定位边框"""
from selenium import webdriver
import time
import base64
from PIL import Image
import cv2
import requests

class Cap_fhhotnews:
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
        driver.save_screenshot('D:\\pythonflask\\jietupicture\\wangyi\\wangyi.png')
        element = driver.find_element_by_class_name('js_hotCmtBlock')
        xPiont = element.location['x']
        yPiont = element.location['y']
        element_width = xPiont + element.size['width']
        element_height = yPiont + element.size['height']
        picture = Image.open('D:\\pythonflask\\jietupicture\\wangyi\\wangyi.png')
        pic = picture.crop((xPiont-10, yPiont, element_width+20, element_height+170))
        pic.save(r'D:\\pythonflask\\jietupicture\\wangyi\\wangyi.png')
        """单条评论加上边框"""
        element = driver.find_element_by_css_selector(
            '#js_cmtContainer > div.js_hotCmtBlock > div.mod-commentNew.js_cmtList > div:nth-child({})'.format(
                int(self.hot_list.index(self.Id)) + 1))
        xPiont = element.location['x']
        yPiont = element.location['y']
        # element_width = xPiont + element.size['width']
        element_height = yPiont + element.size['height']
        image = 'D:\\pythonflask\\jietupicture\\wangyi\\wangyi.png'
        img = cv2.imread(image)
        cv2.rectangle(img, (3, yPiont - 237), (element.size['width'] + 20, element_height - 237), (0, 255, 0),
                      5)  # '237'为'热门跟帖'到页面最上边缘的距离
        cv2.imwrite(image, img)
        image = 'D:\\pythonflask\\jietupicture\\wangyi\\wangyi.png'  # 获取图片的二进制字符串
        with open(image, 'rb') as f:
            strb = base64.b64encode(f.read())
        place = int(self.hot_list.index(self.Id)) + 1
        datadict = {'type': '1', 'taskid': self.taskid, 'title':self.title,'newtime':self.articletime,'zannumber':self.agree,'weizhi':str(place),'url': str(strb, encoding="utf-8")}
        apiurl = 'http://127.0.0.1/Port/getpic.php'
        requests.post(apiurl,data=datadict)
        print('已请求接口')
        return datadict