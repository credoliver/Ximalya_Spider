# -*- coding: utf-8 -*- 
import urllib2
import re
import urllib
album_infos = []
#用于保存专辑信息
albums_url = []
#用于保存各个专辑的页面url
def get_info(urls):
    album_page_req = urllib2.Request(urls)
    album_page_response = urllib2.urlopen(album_page_req)
    album_page = album_page_response.read().decode('utf-8')
#读取专辑页面
    tittle = re.search('_title"><h1>(.*?)</h1>',album_page).groups()[0]
#保存专辑标题信息    
    anchorman_pattern = re.compile(u'username">\s*\n\s*(.*?)\s*\n\s*<i')
    re_anchorman = anchorman_pattern.search(album_page)
    if re_anchorman is None:
        anchorman_pattern = re.compile(u'username">\s*\n\s*(.*?)\s*\n\s*<a')
        re_anchorman = anchorman_pattern.search(album_page)
        anchorman = re_anchorman.groups()[0]
    else:
        anchorman = re_anchorman.groups()[0]
#保存专辑作者信息,由于作者存在大V和普通用户,因此需要构造两个正则表达式来爬取    
    info_pattern = re.compile(u'<article>(.*?)</article')
    re_info = info_pattern.search(album_page)
    if re_info is None:
        info = 'No Info'
    else:
        info = re_info.groups()[0]
#保存专辑简介,有些专辑没有简介则保存为 No Info    
    playCount_pattern = re.compile(u'<span>(.*?)</span>\s+\n\s+次播放')
    re_PlayCount=playCount_pattern.search(album_page)
    if re_PlayCount is None:
        totalPlayCount = '0'
    else:
        totalPlayCount = re_PlayCount.groups()[0]
#保存专辑总播放次数,对于没有播放次数的专辑,将其播放次数设置为No PlayCount        
    album_info = ['tittle:'+tittle,'anchorman:'+anchorman,'info:'+info,totalPlayCount]
    return album_info

def info_mix(album_infos = [],albums_url = []):
    for urls in albums_url:
        album_infos.append(get_info(urls))
#爬取所有于卓老板相关的专辑信息,合并到album_infos中
        
def str_to_int(album_infos = []):
    for infos in album_infos:
        if re.compile(u'万').search(infos[3]) is not None:
            infos[3] = float(re.search('(\d*.\d)',infos[3]).groups()[0])*10000.0
        else:
            infos[3] = float(infos[3])
#将播放量数据中的字符串转换为float格式,便于比较大小
def int_to_str(album_infos = []):
    for infos in album_infos:
        if infos[3]>10000:
            infos[3]='totalPlayCount:'+str(infos[3]/10000.0)+'万'
        else:
            infos[3]='totalPlayCount:'+str(int(infos[3]))
#将比较完大小后的播放数据转换成字符串格式,便于显示


'''
主程序入口------------------------------------
'''
root_page_req = urllib2.Request('http://www.ximalaya.com/search/%E5%8D%93%E8%80%81%E6%9D%BF/t3s3')    
root_page_response = urllib2.urlopen(root_page_req)    
root_page = root_page_response.read()
#读取初始页面,album_infos和album_url分别用于保存专辑详情,专辑页面url

re_album_urls = re.findall('<a\s*href=".*?/album/.*?"',root_page)
for albums in re_album_urls:
    num=re.match('<a\s*href="/(.*?)"',albums).groups()[0]
    albums_url.append('http://www.ximalaya.com/'+num)
#从初始页面爬取专辑的url并保存下来
    
info_mix(album_infos,albums_url)
#将爬取下来的专辑信息合并到album_infos中
str_to_int(album_infos)
album_infos=sorted(album_infos,key=lambda infos:infos[3],reverse=True)
#调用sorted函数对album_infos按照第四个关键字即播放量排序
int_to_str(album_infos)
album_count = len(album_infos)/4
for infos in album_infos:
    for i in range(0,4,1):
        print infos[i],
    print '\n'
#打印爬取的数据




