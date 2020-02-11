# coding=gbk
"""模拟浏览器登录微博账号并更换代理IP"""
import requests
import pymysql
import xlrd
from selenium import webdriver
from proxy_auth import *
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import re

def get_ip():
    try:
        ipapi = 'http://27.223.2.166:28880/api/get'
        iplist = requests.get(ipapi).json()
        ip = iplist['ip'] + ':' + str(iplist['port'])
        serverid = iplist['server_id']
        return ip, serverid
    except Exception:
        return 'error'


def switch_ip(serverid):
    switchurl = f'http://27.223.2.166:28880/api/switch?server_id={serverid}'
    requests.get(switchurl)
    print('Replaced：' + serverid)


def insert_mysql(username, password, cookie_str, uid, nickname):
    db = pymysql.connect('localhost', 'root', '950106', 'wemedia_new')
    cursor = db.cursor()
    sql = "insert into bigdataweibo200 (username, password, cookie, uid, nickname) values (%s, %s, %s, %s, %s)"
    param = (username, password, cookie_str, uid, nickname)
    cursor.execute(sql, param)
    db.commit()
    db.close()


def update_mysql(cookie_str, username, usid):
    db = pymysql.connect('10.0.8.65', 'hzdkpy', 'WSDCWBKxhRKfdYAj', 'hzdkpy')
    cursor = db.cursor()
    sql = "update wbaccount_hd set cookie='{}', uid='{}' where username='{}'".format(cookie_str, usid, username)
    # param = (username, password, cookie_str)
    cursor.execute(sql)
    db.commit()
    db.close()
def update_qun_mysql(cookie_str, username):
    db = pymysql.connect('10.0.8.65', 'qddkpy', 'EYnpbs5LsEKEerAd', 'qddkpy')
    cursor = db.cursor()
    sql = "update qun_info set cookie='{}' where username='{}'".format(cookie_str, username)
    # param = (username, password, cookie_str)
    cursor.execute(sql)
    db.commit()
    db.close()


def add_ip(username, password):
    f = 0
    while f < 10:
        try:
            result = get_ip()
            ip = result[0]
            print(ip)
            serverid = result[1]
            if ip == 'err:8888':
                switch_ip(serverid)
                f += 1
                if f == 10:
                    break
                # time.sleep(15)
            elif ip == 'error':
                f += 1
                if f == 10:
                    break
                time.sleep(2)
            else:
                url = 'https://passport.weibo.cn/signin/login?'
                mobile_emulation = {"deviceName": "iPhone 6"}
                chrome_options = webdriver.ChromeOptions()
                p_path = create_proxyauth_extension(
                    proxy_host=ip[:-5],
                    proxy_port=8888,
                    proxy_username="admin",
                    proxy_password="147852qwe",
                    scheme='http'
                )
                chrome_options.add_extension(p_path)
                chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
                # chrome_options.add_argument('--headless')
                driver = webdriver.Chrome(chrome_options=chrome_options)
                driver.maximize_window()
                driver.get(url)
                time.sleep(2)
                driver.find_element_by_id('loginName').clear()
                driver.find_element_by_id('loginName').send_keys(username)
                driver.find_element_by_id('loginPassword').clear()
                driver.find_element_by_id('loginPassword').send_keys(password)
                # WebDriverWait(driver, 5).until(expected_conditions.visibility_of_element_located((By.ID, 'loginAction')))
                driver.find_element_by_id('loginAction').click()
                time.sleep(1)
                # try:
                #     errmsg = driver.find_element_by_id('errorMsg').text
                #     if errmsg != '':
                #         print(str(username) + errmsg)
                #         driver.close()
                #         break
                # except Exception:
                #     pass
                k = 0
                while k < 5:
                    try:
                        WebDriverWait(driver, 5).until(
                            expected_conditions.visibility_of_element_located(
                                (By.CLASS_NAME, 'geetest_radar_tip_content')))
                        driver.find_elements_by_class_name('geetest_radar_tip_content')[0].click()
                    except Exception:
                        pass
                    try:
                        WebDriverWait(driver, 10).until(EC.title_is('微博'))
                        break
                    except Exception:
                        driver.refresh()
                        driver.refresh()
                        driver.refresh()
                        time.sleep(1)
                    k += 1
                    print(k)
                if k == 5:
                    switch_ip(serverid)
                    driver.quit()
                    break
                time.sleep(1)
                cookies = driver.get_cookies()
                cookie_list = []
                for i in cookies:
                    cookie = i['name'] + '=' + i['value']
                    cookie_list.append(cookie)
                cookie_str = ';'.join(cookie_list)
                print(cookie_str)
                # update_qun_mysql(cookie_str, username)
                # WebDriverWait(driver, 5).until(
                #     expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'lite-iconf-profile')))
                # driver.find_element_by_class_name('lite-iconf-profile').click()
                # try:
                #     WebDriverWait(driver, 20).until(EC.title_contains('的微博'))
                # except Exception:
                #     break
                # nickname = driver.find_elements_by_class_name('m-text-cut')[0].text
                # usid = re.findall('.*/(.*)', driver.current_url)[0]
                # insert_mysql(username=username, password=password, cookie_str=cookie_str, uid=usid, nickname=nickname)
                # update_mysql(cookie_str, username, usid)
                # print(nickname, usid)
                # try:
                #     WebDriverWait(driver, 600).until(EC.title_contains('详细资料'))
                # except Exception:
                #     break
                driver.quit()
                switch_ip(serverid)
                # time.sleep(15)
                break
        except Exception:
            driver.quit()
            switch_ip(serverid)
            f += 1
            if f == 10:
                break
            continue

def run_of_excel():
    df = xlrd.open_workbook('大数据微博采集账号200.xlsx')  # 获取excel中的账号密码
    sheet = df.sheets()[0]
    rows = sheet.nrows
    for r in range(rows):
        username = str(int(sheet.row_values(r)[0]))
        password = sheet.row_values(r)[1]
        print(username)
        add_ip(username, password)

def run_of_mysql():
    db = pymysql.connect('10.0.8.65', 'qddkpy', 'EYnpbs5LsEKEerAd', 'qddkpy')
    cursor = db.cursor()
    sql = "select distinct username, password from qun_info"
    # param = (username, password, cookie_str)
    cursor.execute(sql)
    results = cursor.fetchall()
    for i in results:
        try:
            username = i[0]
            password = i[1]
            print(username)
            add_ip(username, password)
        except Exception as e:
            print(e)
            username = i[0]
            password = i[1]
            print(username)
            add_ip(username, password)
    cursor.close()
    db.close()


def ceshi():
    db = pymysql.connect('localhost', 'root', '950106', 'qddkpy')
    cursor = db.cursor()
    sql = "select username,password from account_ceshi_wh"
    # param = (username, password, cookie_str)
    cursor.execute(sql)
    result = cursor.fetchall()
    sql = "select username,password from account_ceshi_copy1"
    cursor.execute(sql)
    result1 = cursor.fetchall()
    result1 = [i[0] for i in result1]
    for j in result:
        if j[0] not in result1:
            print(j[0])
            add_ip(j[0], j[1])


if __name__ == '__main__':
    # run_of_mysql()
    # ceshi()
    # run_of_excel()
    username = '15634218103'
    password = 'he950106'
    add_ip(username, password)