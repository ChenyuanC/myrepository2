#东方铃奈庵 单线程
import re
import requests
import os
class Thbwiki:
    def __init__(self):
        pass
    def SearchUrl(self,hearder):
        url = 'https://thwiki.cc/%E4%B8%9C%E6%96%B9%E9%93%83%E5%A5%88%E5%BA%B5'
        '''
        <li>第1-3，5-16页：<a rel="nofollow" class="external text" href="http://bbs.nyasama.com/forum.php?mod=viewthread&amp;tid=66621">第四十六话 稗田阿求的哲学 前篇</a>
        <i>（连载于2016年12月26日，Comp Ace 1月号）</i></li>
        '''
        urlDict = {}
        r = requests.get(url, hearder)
        print(r.status_code)
        #print(r.text)
        #正则表达式
        pattern = re.compile('<li.*?rel="nofollow" class="external.*?href=".*?tid=(.*?)".*?>(.*?)</a>.*?</li>', re.S)
        results = re.findall(pattern, r.text)
        for result in results:
            url,page = result
            urlDict.update({page:url})
        return urlDict
    def FindSrc(self, purl, hearder):
        url ='http://bbs.nyasama.com/forum.php?mod=viewthread&tid=' + purl
        print(url)
        r = requests.get(url)
        print(r.status_code)
        context = r.text
        '''<img id="aimg_29380" aid="29380" src="static/image/common/none.gif" 
        zoomfile="http://www.nyasama.com/bsup/nyaup/attachment/forum/201303/05/15281245x4yh503vz9hvvk.jpg" 
        file="http://www.nyasama.com/bsup/nyaup/attachment/forum/201303/05/15281245x4yh503vz9hvvk.jpg" 
        class="zoom" onclick="zoom(this, this.src, 0, 0, 0)" width="600" id="aimg_29380" inpost="1" 
        onmouseover="showMenu({'ctrlid':this.id,'pos':'12'})" />'''
    #     print(context)
        pattern = re.compile('<img.*?zoomfile="(.*?)".*?>', re.S)
        results = re.findall(pattern, context)
#         for result in results:
#             print("序号：%s url:%s"% (results.index(result) + 1, result))
        #print(results)
        return results
    def Download(self, list, savePath,hearder):
        for i in list:
            r = requests.get(i,hearder)
            f = open(savePath  + '/' + str((list.index(i)+1)) + '.jpg', 'wb' )
            f.write(r.content)
            f.close()
            print("success!")
    def CreatF(self, dict,hearder):
        #遍历字典创建文件夹
        for key, value in dict.items():
            savePath = 'E:/东方铃奈庵/' + key
            os.makedirs(savePath)
            urlList = self.FindSrc(value,hearder)
            print(urlList)
            self.Download(urlList, savePath, hearder)
        print("下载完毕！")
hearder = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
thb = Thbwiki()
dict=thb.SearchUrl(hearder)
thb.CreatF(dict,hearder)
list = thb.FindSrc('19720', hearder)
# print(list)
#print(dict)