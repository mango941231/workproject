"""selenim打开指定网页 模拟点击 截图保存"""
from selenium import webdriver
import time
import re
import base64
from PIL import Image
from pyquery import PyQuery as pq
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

class Cap_wyhotnews:
    def __init__(self,url,page):
        self.url = url
        # self.Id = id
        self.wylist = []
        # self.cont = cont
        self.page = int(page)
        self.conpage = 0
        p1 = re.compile(r'.*/(.*).html', re.S)
        cuturl = re.findall(p1, self.url)
        self.pageurl = 'http://comment.tie.163.com/{}.html'.format(cuturl[0])
        self.src = []

    def capture(self):
        # chrome_options = Options()
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('window-size=1920,1080')
        # driver = webdriver.Chrome(chrome_options=chrome_options)
        driver = webdriver.PhantomJS()
        driver.get(self.pageurl)
        # driver.find_element_by_class_name('js-tiejoincount').click()
        # time.sleep(5)
        # driver.switch_to_window(driver.window_handles[1])
        # time.sleep(2)
        driver.maximize_window()
        time.sleep(2)
        # driver.find_element_by_class_name('list-bdy')
        if self.page == 1:
            driver.save_screenshot('F:\\picture\\wangyi\\wangyi.png')
            element = driver.find_element_by_class_name('tie-hot ')
            xPiont = element.location['x']
            yPiont = element.location['y']
            element_width = xPiont + element.size['width']
            element_height = yPiont + element.size['height']
            picture = Image.open('F:\\picture\\wangyi\\wangyi.png')
            pic = picture.crop((xPiont, yPiont, element_width, element_height))
            pic.save(r'F:\\picture\\wangyi\\wangyi.png')
            time.sleep(5)
            image = 'F:\\picture\\wangyi\\wangyi.png'
            with open(image, 'rb') as f:
                strb = base64.b64encode(f.read())
                self.src.append({'url': str(strb,encoding="utf-8")})
            return self.src

        elif self.page > 1:
            driver.save_screenshot('F:\\picture\\wangyi\\wangyi1.png')
            element = driver.find_element_by_class_name('tie-hot ')
            xPiont = element.location['x']
            yPiont = element.location['y']
            element_width = xPiont + element.size['width']
            element_height = yPiont + element.size['height']
            picture = Image.open('F:\\picture\\wangyi\\wangyi1.png')
            pic = picture.crop((xPiont, yPiont, element_width, element_height))
            pic.save(r'F:\\picture\\wangyi\\wangyi1.png')
            time.sleep(5)
            image = 'F:\\picture\\wangyi\\wangyi1.png'
            with open(image, 'rb') as f:
                strb = base64.b64encode(f.read())
                self.src.append({'url': str(strb,encoding="utf-8")})
            for i in range(self.page-1):
                time.sleep(2)
                driver.find_element_by_css_selector('#tie-main > div.tie-hot > div:nth-child(2) > div.list-foot.clearfix > div > ul > li:nth-child(6) > span').click()
                driver.save_screenshot('F:\\picture\\wangyi\\wangyi' + str(i+2) + '.png')
                element = driver.find_element_by_class_name('tie-hot ')
                xPiont = element.location['x']
                yPiont = element.location['y']
                element_width = xPiont + element.size['width']
                element_height = yPiont + element.size['height']
                picture = Image.open('F:\\picture\\wangyi\\wangyi' + str(i+2) + '.png')
                pic = picture.crop((xPiont, yPiont, element_width, element_height))
                pic.save(r'F:\\picture\\wangyi\\wangyi' + str(i+2) + '.png')
                time.sleep(5)
                image = 'F:\\picture\\wangyi\\wangyi' + str(i+2) + '.png'
                with open(image, 'rb') as f:
                    strb = base64.b64encode(f.read())
                    self.src.append({'url': str(strb,encoding="utf-8")})
            return self.src
