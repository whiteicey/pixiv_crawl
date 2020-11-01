from selenium import webdriver
import time
import os
import subprocess
import base64
from lxml import etree
import requests
driver = webdriver.Chrome()
profile_dir = r"C:\Users\ThinkPad\AppData\Local\Google\Chrome\User Data"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("user-data-dir=" + os.path.abspath(profile_dir))
driver = webdriver.Chrome(chrome_options=chrome_options)
thunder_path = 'E:\Thunder\Program\Thunder.exe'

def Url2Thunder(url):
    url = 'AA' + url + 'ZZ'
    url = base64.b64encode(url.encode('utf-8'))
    url = 'thunder://'.encode('utf-8') + url
    thunder_url = url.decode('utf-8')
    return thunder_url


def download_with_thunder(file_url):
    thunder_url = Url2Thunder(file_url)

    if thunder_url.endswith('='):
        pass
        #print(thunder_url)
        #print('Yes')
        

    else:
        thunder_url = thunder_url + "=="
        #print(thunder_url)
    subprocess.call([thunder_path, thunder_url])


driver.get('https://www.pixiv.net/ranking.php?mode=monthly&content=illust')
time.sleep(5)
page = driver.page_source
#print(page)
page = driver.page_source
dom = etree.HTML(page)
ids = dom.xpath('//img[contains(@src,"")]//@src')
#print(ids)
num = 0 
for id in ids:
    if ('240x480' in id) == True:
        #print(id)
        num = num + 1
        data_id = id.strip('https://i.pximg.net/c/240x480/img-maste')
        data_id = data_id.strip('r/')
        #print(data_id)
        data_id = data_id.strip('master1200.jpg')
        data_id = data_id.strip('_')
        #print(data_id)
        img_url1 = 'https://i.pximg.net/img-original/' + data_id + '.png'
        img_url2 = 'https://i.pximg.net/img-original/' + data_id + '.jpg'
        print(img_url1)
        print(img_url2)
        download_with_thunder(img_url2)
        download_with_thunder(img_url1)
        #https://i.pximg.net/c/240x480/img-master/img/2020/10/23/00/30/00/85177342_p0_master1200.jpg
        #https://i.pximg.net/img-original/img/2020/10/23/00/30/00/85177342_p0.jpg
print(num)