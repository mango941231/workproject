from selenium import webdriver
import time
pageurl = 'https://weibo.com/1337970873/H7WMw1dVC?filter=hot&root_comment_id=0&type=comment#_rnd1545209834752'
driver = webdriver.PhantomJS()
driver.get(pageurl)
time.sleep(5)
# driver.switch_to.frame('commentIframe')
element = driver.find_element_by_css_selector('div.repeat_list > div:nth-child(2) > div > div > div:nth-child(1)')
xPiont = element.location['x']
yPiont = element.location['y']
element_width = xPiont + element.size['width']
element_height = yPiont + element.size['height']
print(xPiont,yPiont)
print(element.size['width'],element.size['height'])
