# 东方三月精 多线程
import requests
import re
import threading
import os

#获得页面的的话数的url
def praUrl():
    url = 'https://thwiki.cc/%E4%B8%9C%E6%96%B9%E4%B8%89%E6%9C%88%E7%B2%BE_%EF%BD%9E_Eastern_and_Little_Nature_Deity.'
    r = requests.get(url)
    context = r.text
    urlDict = {}
    #正则表达式
    pattern = re.compile('<li.*?rel="nofollow" class="external.*?href=".*?tid=(.*?)".*?>(.*?)</a>.*?</li>', re.S)
    results = re.findall(pattern, r.text)
    for result in results:
        url ,page = result
        urlDict.update({page:url})
    return urlDict
#保存图片方法
def saveImg(list, savePath):
    print(savePath + '正在下载...')
    for src in list:
        r = requests.get(src)
        with open(savePath + '/' + str((list.index(src)+1)) + '.jpg', 'wb') as f:
            f.write(r.content)
    print(savePath + '下载完成！')
#进入每话的链接得到图片链接
def getImgSrc(floderName, pageUrl, savePath):
    floderPath = savePath + '/' + floderName
    os.makedirs(floderPath)
    pUrl = 'http://bbs.nyasama.com/forum.php?mod=viewthread&tid=' + pageUrl
    r = requests.get(pUrl)
    context = r.text
    pattern = re.compile('<img.*?zoomfile="(.*?)".*?>', re.S)
    results = re.findall(pattern, context)
    saveImg(results, floderPath)

#创建文件夹下载
'''def mkdirFloders(dict, savePath):
    for key, value in dict.items():
        endPath = savePath + key
        os.makedirs(endPath)
        #保存图片
        getImgSrc(value, endPath)'''
#多线程用到的列表
threads = []

dict = praUrl()
#创建多线程
for key,value in dict.items():
    t = threading.Thread(target = getImgSrc,args = (key, value, 'E:/东方三月精一'))
    threads.append(t)
for t in threads:
    t.start()
for t in threads:
    t.join()

#     print (results)
    
# getImgSrc("37069","1")

# print(dict)