"""selenim打开指定网页 模拟点击 截图保存 （2018/12/18 改动：热评条数准确 热评加边框定位）"""
from selenium import webdriver
import time
import re
import base64
from PIL import Image
import cv2
import requests

class Cap_wyhotnews:
    def __init__(self, url, hotlist, ti, Id, title, articletime, agree):
        self.url = url
        self.taskid = ti
        self.Id = Id
        self.wylist = []
        self.hot_list = hotlist
        self.conpage = 0
        p1 = re.compile(r'.*/(.*).html', re.S)
        cuturl = re.findall(p1, self.url)
        self.pageurl = 'http://comment.tie.163.com/{}.html'.format(cuturl[0])
        self.src = []
        self.title = title
        self.articletime = articletime
        self.agree = agree
        self.place = ''
    def capture(self):
        driver = webdriver.PhantomJS()
        driver.maximize_window()
        driver.get(self.pageurl)
        time.sleep(5)
        if self.Id in self.hot_list[0:10]:
            print('评论位于第一页')
            cutlist = list(self.hot_list[0:10])
            driver.save_screenshot('D:\\pythonflask\\jietupicture\\wangyi\\wangyi.png')
            element = driver.find_element_by_css_selector('#tie-main > div.tie-hot')
            xPiont = element.location['x']
            yPiont = element.location['y']
            element_width = xPiont + element.size['width']
            element_height = yPiont + element.size['height']
            picture = Image.open('D:\\pythonflask\\jietupicture\\wangyi\\wangyi.png')
            pic = picture.crop((xPiont, yPiont, element_width, element_height))
            pic.save(r'D:\\pythonflask\\jietupicture\\wangyi\\wangyi.png')
            """单条评论加上边框"""
            element = driver.find_element_by_css_selector(
                '#tie-main > div.tie-hot > div:nth-child(2) > div.list-bdy > div:nth-child({})'.format(int(cutlist.index(self.Id))+1))
            xPiont = element.location['x']
            yPiont = element.location['y']
            # element_width = xPiont + element.size['width']
            element_height = yPiont + element.size['height']
            image = 'D:\\pythonflask\\jietupicture\\wangyi\\wangyi.png'
            img = cv2.imread(image)
            cv2.rectangle(img, (3, yPiont - 237), (element.size['width'] - 5, element_height - 237), (0, 255, 0), 5)    # '237'为'热门跟帖'到页面最上边缘的距离
            cv2.imwrite(image, img)
            self.place = str(int(cutlist.index(self.Id))+1)

        elif self.Id in self.hot_list[10:20]:
            print('评论位于第二页')
            cutlist = list(self.hot_list[10:20])
            driver.find_element_by_css_selector(
                '#tie-main > div.tie-hot > div:nth-child(2) > div.list-foot.clearfix > div > ul > li:nth-child(6) > span').click()
            time.sleep(2)
            driver.save_screenshot('D:\\pythonflask\\jietupicture\\wangyi\\wangyi.png')
            element = driver.find_element_by_class_name('tie-hot ')
            xPiont = element.location['x']
            yPiont = element.location['y']
            element_width = xPiont + element.size['width']
            element_height = yPiont + element.size['height']
            picture = Image.open('D:\\pythonflask\\jietupicture\\wangyi\\wangyi.png')
            pic = picture.crop((xPiont, yPiont, element_width, element_height))
            pic.save(r'D:\\pythonflask\\jietupicture\\wangyi\\wangyi.png')
            """为单条评论加上边框"""
            element = driver.find_element_by_css_selector(
                '#tie-main > div.tie-hot > div:nth-child(2) > div.list-bdy > div:nth-child({})'.format(
                    int(cutlist.index(self.Id))+1))
            xPiont = element.location['x']
            yPiont = element.location['y']
            # element_width = xPiont + element.size['width']
            element_height = yPiont + element.size['height']
            image = 'D:\\pythonflask\\jietupicture\\wangyi\\wangyi.png'
            img = cv2.imread(image)
            cv2.rectangle(img, (3, yPiont - 237), (element.size['width'] - 5, element_height - 237), (0, 255, 0), 5)
            cv2.imwrite(image, img)
            self.place = str(int(cutlist.index(self.Id)) + 1)
        elif self.Id in self.hot_list[20:30]:
            print('评论位于第三页')
            cutlist = list(self.hot_list[20:30])
            driver.find_element_by_css_selector('#tie-main > div.tie-hot > div:nth-child(2) > div.list-foot.clearfix > div > ul > li:nth-child(4) > span').click()
            time.sleep(2)
            driver.save_screenshot('D:\\pythonflask\\jietupicture\\wangyi\\wangyi.png')
            element = driver.find_element_by_class_name('tie-hot ')
            xPiont = element.location['x']
            yPiont = element.location['y']
            element_width = xPiont + element.size['width']
            element_height = yPiont + element.size['height']
            picture = Image.open('D:\\pythonflask\\jietupicture\\wangyi\\wangyi.png')
            pic = picture.crop((xPiont, yPiont, element_width, element_height))
            pic.save(r'D:\\pythonflask\\jietupicture\\wangyi\\wangyi.png')
            """单条评论加上边框"""
            element = driver.find_element_by_css_selector(
                '#tie-main > div.tie-hot > div:nth-child(2) > div.list-bdy > div:nth-child({})'.format(
                    int(cutlist.index(self.Id))+1))
            xPiont = element.location['x']
            yPiont = element.location['y']
            # element_width = xPiont + element.size['width']
            element_height = yPiont + element.size['height']
            image = 'D:\\pythonflask\\jietupicture\\wangyi\\wangyi.png'
            img = cv2.imread(image)
            cv2.rectangle(img, (3, yPiont - 237), (element.size['width'] - 5, element_height - 237), (0, 255, 0), 5)
            cv2.imwrite(image, img)
            self.place = str(int(cutlist.index(self.Id)) + 1)
        elif self.Id in self.hot_list[30:]:
            print('评论位于第四页')
            cutlist = list(self.hot_list[30:])
            driver.find_element_by_css_selector('#tie-main > div.tie-hot > div:nth-child(2) > div.list-foot.clearfix > div > ul > li:nth-child(5) > span').click()
            time.sleep(2)
            driver.save_screenshot('D:\\pythonflask\\jietupicture\\wangyi\\wangyi.png')
            element = driver.find_element_by_class_name('tie-hot ')
            xPiont = element.location['x']
            yPiont = element.location['y']
            element_width = xPiont + element.size['width']
            element_height = yPiont + element.size['height']
            picture = Image.open('D:\\pythonflask\\jietupicture\\wangyi\\wangyi.png')
            pic = picture.crop((xPiont, yPiont, element_width, element_height))
            pic.save(r'D:\\pythonflask\\jietupicture\\wangyi\\wangyi.png')
            """单条评论加上边框"""
            element = driver.find_element_by_css_selector(
                '#tie-main > div.tie-hot > div:nth-child(2) > div.list-bdy > div:nth-child({})'.format(
                    int(cutlist.index(self.Id))+1))
            # xPiont = element.location['x']
            yPiont = element.location['y']
            # element_width = xPiont + element.size['width']
            element_height = yPiont + element.size['height']
            image = 'D:\\pythonflask\\jietupicture\\wangyi\\wangyi.png'
            img = cv2.imread(image)
            cv2.rectangle(img, (3, yPiont - 237), (element.size['width'] - 5, element_height - 237), (0, 255, 0), 5)
            cv2.imwrite(image, img)
            self.place = str(int(cutlist.index(self.Id)) + 1)
        time.sleep(5)
        image = 'D:\\pythonflask\\jietupicture\\wangyi\\wangyi.png'
        with open(image, 'rb') as f:
            strb = base64.b64encode(f.read())
        datadict = {'type': '1', 'taskid': self.taskid, 'title': self.title, 'newtime': self.articletime,
                    'zannumber': self.agree, 'weizhi': str(self.place), 'url': str(strb, encoding="utf-8")}
        apiurl = 'http://127.0.0.1:888/Port/getpic.php'
        requests.post(apiurl, data=datadict)
        print('已请求接口')
        return datadict
