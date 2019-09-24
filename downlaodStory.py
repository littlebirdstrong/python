#!/usr/bin/python3
# -*- coding:utf-8 -*-
__author__ = 'wangyongwei'
__project__ = 'PaChong'
import requests
from bs4 import BeautifulSoup
import sys
import os
'''
下载笔趣看小说
'''
class downLoadStory(object):

    """
    初始化函数
    server:服务器地址
    target:当前下载小说的地址
    """
    def __init__(self,server,target):
        self.server = server
        self.target = target
        self.filename = ""

    """
    获取下载的章节地址
    把章节和地址返回到字典中
    """
    def get_downLoad_url(self):
        target = self.target
        res = requests.get(target)
        res.encoding = res.apparent_encoding
        html = res.text
        # print(html)
        bf = BeautifulSoup(html, 'html.parser')
        texts = bf.find_all('title')
        title = texts[0].string
        self.filename = title[0:title.index('_')]
        listmain = bf.find_all('div', class_='listmain')
        #print(listmain)
        a_href_bf = BeautifulSoup(str(listmain[0]), 'html.parser')
        a_hrefs = a_href_bf.find_all('a')
        # print(a_hrefs)
        all_list_url = {}
        for each in a_hrefs:
            # print(each.string, server + each.get('href'))
            href = self.server + each.get('href')
            all_list_url.update({each.string: href})
        return all_list_url


    """
    根据url获取章节内容
    """
    def get_context(self,target):
            res = requests.get(url=target)
            res.encoding = res.apparent_encoding  # 根据返回的body解析
            html = res.text
            bf = BeautifulSoup(html, 'html.parser')
            texts = bf.find_all('div', class_='showtxt')
            text = texts[0].text.replace('　　', '\n')
            return text
    """
    下载
    filename: 文件名
    text:下载内容
    """
    def writer(self,filename,text,key):
        path = os.getcwd()
        filename =self.filename+'.txt'
        with open(filename, 'a', encoding='utf-8') as f:  # 只能追加
                f.writelines(key)
                f.write('\n\n')
                f.writelines(text)
                f.write('\n\n')






"""主函数"""
if __name__ == '__main__':
    d1 = downLoadStory('https://www.biqukan.com','https://www.biqukan.com/10_10567')
    url_dict = {}
    url_dict = d1.get_downLoad_url()
    print('Starting...')
    length = len(url_dict)
    num = 0
    for key in url_dict:
        d1.writer(d1.filename,d1.get_context(url_dict[key]),key)
        num += 1
        sys.stdout.write('Finshed%.3f%%' % float(num/length)+'\r')
    print('Success')
