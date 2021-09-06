import os
import re
import sys
import winreg
import zipfile
from pathlib import Path
import requests
from selenium import webdriver
import time
import os
from lxml import etree
from win32com.client import Dispatch

python_root = Path(sys.executable).parent  # python安装目录
base_url = 'http://npm.taobao.org/mirrors/chromedriver/'  # chromedriver在国内的镜像网站
version_re = re.compile(r'^[1-9]\d*\.\d*.\d*')  # 匹配前3位版本信息


def get_chrome_version():
    """通过注册表查询Chrome版本信息: HKEY_CURRENT_USER\SOFTWARE\Google\Chrome\BLBeacon: version"""
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'SOFTWARE\Google\Chrome\BLBeacon')
        value = winreg.QueryValueEx(key, 'version')[0]
        return version_re.findall(value)[0]
    except WindowsError as e:
        return '0.0.0'  # 没有安装Chrome浏览器


def get_chrome_driver_version():
    try:
        result = os.popen('chromedriver --version').read()
        version = result.split(' ')[1]
        return '.'.join(version.split('.')[:-1])
    except Exception as e:
        return '0.0.0'  # 没有安装ChromeDriver


def get_latest_chrome_driver(chrome_version):
    url = f'{base_url}LATEST_RELEASE_{chrome_version}'
    latest_version = requests.get(url).text
    download_url = f'{base_url}{latest_version}/chromedriver_win32.zip'
    # 下载chromedriver zip文件
    response = requests.get(download_url)
    local_file = python_root / 'chromedriver.zip'
    with open(local_file, 'wb') as zip_file:
        zip_file.write(response.content)

    # 解压缩zip文件到python安装目录
    f = zipfile.ZipFile(local_file, 'r')
    for file in f.namelist():
        f.extract(file, python_root)
    f.close()

    local_file.unlink()  # 解压缩完成后删除zip文件


def check_chrome_driver_update():
    chrome_version = get_chrome_version()
    driver_version = get_chrome_driver_version()
    if chrome_version == driver_version:
        print('No need to update')
    else:
        try:
            get_latest_chrome_driver(chrome_version)
        except Exception as e:
            print(f'Fail to update: {e}')



check_chrome_driver_update()
time.sleep(5)
driver = webdriver.Chrome()
profile_dir = r"C:/Users/12697/AppData/Local/Google/Chrome/User Data"#这里写google的userdata地址
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("user-data-dir=" + os.path.abspath(profile_dir))
driver = webdriver.Chrome(chrome_options=chrome_options)
thunder = Dispatch("ThunderAgent.Agent64.1")
driver.get('https://www.pixiv.net/ranking.php?mode=monthly&content=illust')
time.sleep(50)
page = driver.page_source
page = driver.page_source
dom = etree.HTML(page)
ids = dom.xpath('//img[contains(@src,"")]//@src')
num = 0
for id in ids:
    if ('240x480' in id) == True:
        num = num + 1
        data_id = id.strip('https://i.pximg.net/c/240x480/img-maste')
        data_id = data_id.strip('r/')
        data_id = data_id.strip('master1200.jpg')
        data_id = data_id.strip('_')
        img_url1 = 'https://i.pximg.net/img-original/' + data_id + '.png'
        img_url2 = 'https://i.pximg.net/img-original/' + data_id + '.jpg'
        thunder.AddTask(img_url1)
        thunder.AddTask(img_url2)
print(num)
thunder.CommitTasks()