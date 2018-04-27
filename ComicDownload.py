#风之漫画爬虫最终版
import requests
import re
import os
import time

class ComicDownload:
    
    #类初始化
    def __init__(self):
        pass
    
    #解析该漫画的首页方法返回一个“话数”：“url”的字典
    def getPageUrl(self, url, hearder):
        #请求页面，获得网页源代码，正则表达式匹配
        r = requests.get(url, hearder)
        urlContext = r.text
        print(r.status_code)
        #正则表达式
        pattern = re.compile('<li.*?href="(.*?)".*?title="(.*?)">.*?</li>', re.S)
        results = re.findall(pattern, urlContext)
        
        #创建空字典
        pageDict = {}
        
        #将每话的url添加到字典中返回
        for result in results:
            pUrl, page = result
             #print('http://manhua.fzdm.com/56/' + url, page)
            pageDict.update({ page : url + pUrl })
        #print(pageDict)
        #删除 分享到QQ空间 的键
        del pageDict['分享到QQ空间']
        return pageDict
    
    #遍历每话的url，获得每话共有多少P，及每P的url
    def getPicUrl(self, pageUrl, hearder):
        #由http://manhua.fzdm.com/56/262/ 拼成 http://manhua.fzdm.com/56/001/index_xx.html
        midStr = 'index_'
        endStr = '.html'
        #返回的list
        pList = []
        #拼接遍历
        for i in range( 0, 60, 1 ):
            pUrl = pageUrl + midStr + str(i) + endStr
            r = requests.get(pageUrl, hearder)
            #判断是否还有下一P
            if(r.status_code == 200):
                pList.append(pUrl)
                #休眠半秒钟
                time.sleep(0.5)
        #返回list
        return pList
    
    #每一P的地址，解析图片的地址
    def getImgSrc(self, list, hearder):
        #每个图片的的src地址list
        imgSrc = []
        #getPicUrl得到的每话list，遍历得到图片的地址
        for url in list:
            r = requests.get(url, hearder)
            context = r.text
            #<img src="http://183.91.33.78/p1.xiaoshidi.net/2018/02/06040143703960.jpg" id="mhpic" alt="七原罪253话" onerror="nofind();">
             #图片src嵌在js代码中 mhurl1 = "2018/02/06040143704254.jpg"
            #正则表达式
            pattern = re.compile('mhurl1 = "(.*?\.jpg)"', re.S)
            result = re.search(pattern, context)
            if(result !=None):
                imgStr = result.group(1)
                if(imgSrc != None):
                    print(imgSrc)
                    imgSrc2 = 'http://183.91.33.78/p1.xiaoshidi.net/' + imgStr
                    #添加到src地址的list
                    imgSrc.append(imgSrc2)
        return imgSrc
   
    #保存图片
    def saveImg(self, list,savePath, hearder):
        #遍历list获得每张图片的src
        for imgSrc2 in list:
            try:
                r = requests.get(imgSrc2, hearder)
                #保存
                f = open(savePath  + '/' + str(list.index(imgSrc2)+1) + '.jpg', 'wb' )
                f.write(r.content)
                f.close()
                print('success')
                #休眠半秒
                time.sleep(0.5)
            except Exception as e:
                print(repr(e))
        
  #创建目录及根据字典的值url遍历下载
    def imgDownload(self, dict, hearder):
        #遍历字典创建目录
        for title, pageUrl in dict.items():
            savePath = 'F:/code/pic/' + title
            os.makedirs(savePath)
            #调用getPicUrl方法
            pList = self.getPicUrl(pageUrl, hearder)
            print(pList)
            #调用saveImg获得存储图片的list
            imgSrc = self.getImgSrc(pList, hearder)
            print(imgSrc)
            #调用saveImg 保存图片
            self.saveImg(imgSrc, savePath, hearder)
            print('completed!')
c = ComicDownload()
url = 'http://manhua.fzdm.com/56/'
hearder = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
pageDict = c.getPageUrl(url, hearder)
c.imgDownload(pageDict, hearder)