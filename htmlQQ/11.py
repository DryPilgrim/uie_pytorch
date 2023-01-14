import re, urllib
from urllib.request import urlopen, Request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time,re
from selenium.webdriver.support.ui import WebDriverWait


# 使用webdriver
options = Options()
options.add_argument('--headless')

chrome_driver="D:\\APPS\\Anaconda\\anaconda3\\envs\\allOne\\chromedriver.exe"
driver = webdriver.Chrome(executable_path=chrome_driver, options=options)
driver.get('http://a.mp.uc.cn/media?mid=00f52ad73e534153a7417b579d9aa494')
time.sleep(5)
# wait=WebDriverWait(driver,10)
resp=driver.page_source
with open('html\\amp.txt','w') as f:
    f.write(resp)
driver.close()

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
url = "https://user.qzone.qq.com/1437350694?source=namecardhoverqzone"
# ret = Request(url, headers=headers)
# res = urlopen(ret)
# aa = res.read().decode('gbk',"ignore")
# with open('html/'+url.split('//')[-1].split("/")[0]+'.txt','w') as f:
#     f.write(aa)

def get_txt(atxt):
    print("=========>>正则处理网页...")
    with open(atxt) as file_object:
        contents = file_object.read()
        #^<.*>$
        #<.*?>
        # contents = re.sub(r'<.*?>', '', contents)
        ##.*
        #var.*
        #\.\w*.*
        # print(contents.rstrip())
        # 把html中的换行符，去掉，也就是替换成空字符串，因为.不能匹配到换行符
        # contents = re.sub(r'\n', '', contents)
        # contents = re.sub(r'\t', '', contents)
        """
        match()函数是从string的开始位置查找，找不到返回None。search()会扫描整个string，然后返回第一个成功的匹配。
        """
        # print(re.search(r'src=\"http.*', contents).group())
        
    jpg_all_tmp = re.findall(r'src="http.*', contents)
    with open('html\\jpg_all_1.txt','w') as f:
        f.write(str(jpg_all_tmp))

    jpg_all = re.findall(r'src="(.*?) data-loaded', str(jpg_all_tmp))
    with open('html\\jpg_all_2.txt','w') as f:
        f.write(str(jpg_all))

        
    # uie(contents)
def get_jpg():
    import requests
    url = 'http://photogz.photo.store.qq.com/psc?/V54OHTx73RXaWf13HxnF1YGhCl16rjdd/h6xaDFri07erS800s2XKmJc1RJE96nabRdEZ2WI3Q2NlQ6jnGwWp*O5Dqk4UmdFR4lyCHl3pMta3DdMzmau0L8yWIvuuqS9H5fwLU36zN69vy.dTepS4d6MTbA7l*CQB/mnull&amp;bo=3wUnDt8FJw4BByA!&amp;rf=photolist&amp;t=5'
    headers = {'Referer':'Referer: https://user.qzone.qq.com/','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}
    res = requests.get(url, headers=headers)
    # res = urllib.request.Request(url)
    # res = urllib.request.urlopen(res)
    with open('test.jpg', 'wb') as f:
        f.write(res.content)
        f.close()

def main():
    # get_txt("html\\user.qzone.qq.com.txt")
    # get_jpg()
    pass

# main()