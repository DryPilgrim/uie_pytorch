#coding: utf-8
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import xlwt, re, os
from uie_predictor import UIEPredictor
from pprint import pprint
from lxml import etree


host_list=[
    "http://a.mp.uc.cn/media?mid=00f52ad73e534153a7417b579d9aa494",
    "http://ask.zol.com.cn/me/cuiyunnan/",
    "https://m.weibo.cn/u/2803301701",
    "https://k.sina.cn/media_m_1585173.html",
    "https://www.zhihu.com/people/zhi-hu-ri-bao-51-41?utm_saource=quark_banner",
    "https://tieba.baidu.com/home/main?id=tb.1.7facc916.bR4WouWOWMXkl1Kkdi9XUw",
    "https://haokan.baidu.com/author/1570695486022261",
    "https://baijiahao.baidu.com/u?app_id=1570695486022261",
    "https://www.ixigua.com/home/77121077814/",
    "https://www.mafengwo.cn/u/10024.html"
]
schema =['用户名','作者','简介','签名', 'ip属地','粉丝数','关注数','获赞数','内容领域','作品']

def get_html(url):
    from selenium.webdriver.chrome.options import Options
    from selenium import webdriver
    import time

    print("=========>>爬取网页...")
    # 使用webdriver
    options = Options()
    options.add_argument('--headless')

    chrome_driver="./chromedriver" #路径不能省略'./'
    driver = webdriver.Chrome(executable_path=chrome_driver, options=options)
    driver.get(url)
    time.sleep(4)
    # wait=WebDriverWait(driver,10)
    resp=driver.page_source

    with open('html/'+url.split('//')[-1].split("/")[0]+'.txt','w') as f:
        f.write(resp)
    # with open('html/'+url.split('//')[-1].split("/")[0]+'.txt','r+') as f:    
    #     content = f.read()    
    #     f.seek(0) #get to the first position
    #     f.write("#coding:utf-8" + '\n' + content)
    
    driver.close()

    # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
    # ret = Request(url, headers=headers)
    # res = urlopen(ret)
    # aa = res.read().decode('gbk',"ignore")
    # with open('html/'+url.split('//')[-1].split("/")[0]+'.txt','w') as f:
    #     f.write(aa)

    # soup = BeautifulSoup(aa,'html.parser')
    # with open('11.txt','w') as f:
    #     f.write(soup.text)

    # comment = soup.select('tr td.title a')
    # for i in range(0,len(comment)):
    #     comment[i] = comment[i].get('title')

def re_uie(atxt):
    print("=========>>正则处理网页...")
    with open(atxt,encoding='utf-8') as file_object:
        contents = file_object.read()
        #^<.*>$
        #<.*?>
        contents = re.sub(r'<.*?>', '', contents)
        #匹配括号里的内容包括括号
        # contents = re.sub(r'(\{)[^}]*(\})', '', contents)
        # contents = re.sub(r'(\[)[^}]*(\])', '', contents)
        # contents = re.sub(r'(\()[^}]*(\))', '', contents)
        # contents = re.sub(r'(\.)[^}]*(\.)', '', contents)
        # contents = re.sub(r'(?m)^\s*#.*$', '', contents)
        # contents = re.sub(r'(?m)^\s*var.*$', '', contents)
        # contents = re.sub(r'(?m)\s*[.!@/${}*:-].*$', '', contents)
        # contents = re.sub(r'(?m)^.*function.*$', '', contents)
        # contents = re.sub(r'(?m)^\s*back.*$', '', contents)
        # contents = re.sub(r'(?m)^\s*dia.*$', '', contents)
        # contents = re.sub(r'\{.*\}', '', contents)
        # contents = re.sub(r'[#.]+[\w\s.,-:]*', '', contents)
        # contents = re.sub(r'var \w* = [.\t";\[\]\w\'\n{}+=\-:,()]*', '', contents)
        # contents = re.sub(r"\{[\n\s\w;:,!()\r\t\f\[\b\];\"'\+$=]+\}", '', contents)
        # contents = re.sub(r"[#.]+[\w* .,-{}'()]*", '', contents)
        # contents = str(re.findall(r'<.*>(.*?)</.*>', contents))
        # contents = re.sub(r'\n{2,}', '\n', contents)
    with open(atxt[0:-4] +'_1.txt','w') as f:
        f.write(contents)
    ##.*
    #var.*
    #\.\w*.*
    # print(contents.rstrip())
    """
    match()函数是从string的开始位置查找，找不到返回None。search()会扫描整个string，然后返回第一个成功的匹配。
    """
    # print(re.search("cuiyunnan", contents).group())
    uie(contents)

def xpath_uie(atxt):
    with open(atxt) as file_object:
        contents = file_object.read()
    tree = etree.HTML(contents)
    text = ' '.join(tree.xpath('/html/body/div[1]/div/main/div/div[1]/div/div[2]/div/div[2]/div[1]/h1/span/text()'))
    print(text)

def uie(body):
    print("=========>>网页信息抽取...")
    ie = UIEPredictor(model='uie-base', schema=schema)
    pprint(ie(body)) # Better print results using pprint

def main():         
    os.system("rm html/*")
    for host in host_list:
        txt='html/'+host.split('//')[-1]+'.txt'#.split("/")[0]
        #--step1 爬取html源代码
        if not os.path.exists(txt):
            print('not exist: ',txt)
            try:
                get_html(host)
            except:
                pass
        #--step2 提取文本内容
        if os.path.exists(txt):
            try:
                re_uie(txt)
            except:
                pass
    # re_uie('html/a.mp.uc.cn.txt')

main()