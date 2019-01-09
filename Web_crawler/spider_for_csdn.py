# encoding: utf-8
'''
@author: season
@contact: seasonwang@insightzen.com

@file: spider_for_csdn.py
@time: 2018/10/16 21:32
@desc:
使用时候，需要替换博客链接

'''
import io
import os
import sys
import urllib
from urllib.request import urlopen
from urllib import request
from bs4 import BeautifulSoup
import datetime
import random
import re
from lxml import etree
import socket

import sys
import os
currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl, os.pardir))
#print(parentUrl)
sys.path.append(parentUrl)

from Database import CSDN_Blog

socket.setdefaulttimeout(5000)  # 设置全局超时函数

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')

my_headers = [
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)"
]

headers1 = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
headers2 = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'}
headers3 = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}



def getArticleLinks(pageUrl,articles):
    # 设置代理IP
    # 代理IP可以上http://ip.zdaye.com/获取
    proxy_handler = urllib.request.ProxyHandler({'post': '49.51.195.24:1080'})
    proxy_auth_handler = urllib.request.ProxyBasicAuthHandler()
    opener = urllib.request.build_opener(urllib.request.HTTPHandler, proxy_handler)
    urllib.request.install_opener(opener)
    # 获取网页信息
    req = request.Request(pageUrl, headers=headers1 or headers2 or headers3)
    html = urlopen(req)
    bsObj = BeautifulSoup(html.read(), "html.parser")


    for articlelist in bsObj.findAll("h4"):  # 正则表达式匹配每一篇文章链接(比较硬编码h4 这个四级标题里面藏了所有链接)
        # print(articlelist)
        if 'href' in articlelist.a.attrs:
            if articlelist.a.attrs["href"] not in articles:
                # 遇到了新界面
                newArticle = articlelist.a.attrs["href"]
                # print(newArticle)
                articles.add(newArticle)
                #print(newArticle)


# # 得到CSDN博客每一篇文章的文字内容,title-article 为标题，id="article_content" 里面为文章内容
# def getArticleText(articleUrl,articletitle):
#     # 设置代理IP
#     # 代理IP可以上http://ip.zdaye.com/获取
#     proxy_handler = urllib.request.ProxyHandler({'https': '120.132.52.89:8888'})
#     proxy_auth_handler = urllib.request.ProxyBasicAuthHandler()
#     opener = urllib.request.build_opener(urllib.request.HTTPHandler, proxy_handler)
#     urllib.request.install_opener(opener)
#     # 获取网页信息
#     req = request.Request(articleUrl, headers=headers1 or headers2 or headers3)
#     print(articleUrl)
#     html = urlopen(req)
#     bsObj = BeautifulSoup(html.read(), "html.parser")
#     # 获取文章的文字内容
#     for textlist in bsObj.findAll(articletitle):  # 正则表达式匹配文字内容标签
#         print(textlist.get_text())
#         # data_out(textlist.get_text())






# def getPageLinks(bokezhuye,pages):
#     # 设置代理IP
#     # 代理IP可以上http://ip.zdaye.com/获取
#     proxy_handler = urllib.request.ProxyHandler({'post': '49.51.195.24:1080'})
#     # proxy_auth_handler = urllib.request.ProxyBasicAuthHandler()
#     opener = urllib.request.build_opener(urllib.request.HTTPHandler, proxy_handler)
#     urllib.request.install_opener(opener)
#     # 获取网页信息
#     req = request.Request(bokezhuye, headers=headers1 or headers2 or headers3)
#     html = urlopen(req)
#     bsObj = BeautifulSoup(html.read(), "html.parser")
#     # 获取当前页面(第一页)的所有文章的链接
#     getArticleLinks(bokezhuye)
#     # 去除重复的链接
#
#     for pagelist in bsObj.findAll("a", href=re.compile("^/([A-Za-z0-9]+)(/article)(/list)(/[0-9]+)*$")):  # 正则表达式匹配分页的链接
#         if 'href' in pagelist.attrs:
#             if pagelist.attrs["href"] not in pages:
#                 # 遇到了新的界面
#                 newPage = pagelist.attrs["href"]
#                 # print(newPage)
#                 pages.add(newPage)
#                 # 获取接下来的每一个页面上的每一篇文章的链接
#                 newPageLink = "http://blog.csdn.net/" + newPage
#                 getArticleLinks(newPageLink)
#                 # # 爬取每一篇文章的文字内容
#                 # for articlelist in articles:
#                 #     newarticlelist = "http://blog.csdn.net/" + articlelist
#                 #     print(newarticlelist)
#                 #     getArticleText(newarticlelist)






#windows 创建文件替换特殊字符
def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    return new_title.replace('\r','').replace('\n','').replace('\t','')

#csdn 的网页解析
def get_Content(url,contend_box_id,title_id,contend_id):
    try:
        randdom_header = random.choice(my_headers)

        req = urllib.request.Request(url)

        req.add_header("User-Agent", randdom_header)
        req.add_header("GET", url)

        response = urllib.request.urlopen(req)
    # html = response.read().decode('utf-8')
    #     # print(html)
        page_content = response.read()
        bsObj = BeautifulSoup(page_content, "html.parser")
        etree_obj = etree.HTML(page_content)
    # 获取文章的文字内容
    # 获取网页信息
    #此处逻辑应为：首先获取文章box 的id 之后获取，title 的，之后是content 的
    # 将每一篇博客分别保存为一个文件

        #链接最后
        id = url.split('/')[-1]

        title = bsObj.findAll(name='h1', attrs={'class': title_id})
        str_title = validateTitle(title[0].get_text() + '.txt')

        #contend =
        #create_time =bsObj.findAll(name='div', attrs={'class': 'article-bar-top'})[0]
        xpath_create_time = '''// *[ @ id = "mainBox"] / main / div[1] / div / div / div[2] / div[1] / span[1]'''
        from src import assistance_tool
        create_time = assistance_tool.clean_csdn_date(etree_obj.xpath(xpath_create_time)[0].text)
        xpath_click_number ='''//*[@id="mainBox"]/main/div[1]/div/div/div[2]/div[1]/span[2]'''

        click_number =assistance_tool.clean_csdn_date(etree_obj.xpath(xpath_click_number)[0].text)
        xpath_comment_number = '''//*[@id="mainBox"]/main/div[2]/div[2]/div[1]/p[3]/span'''
        comment_number =assistance_tool.clean_csdn_date(etree_obj.xpath(xpath_comment_number)[0].text)
        # label =

        print(str_title.encode('gbk'))
        f_blog = open('blog//' + str_title, 'w', encoding='utf-8')

        for content_box in bsObj.findAll(name='div',attrs={'class':contend_box_id}):  # 正则表达式匹配博客包含框 标签

            for contend in bsObj.findAll(name='div',id = contend_id):#内容,注意此处用了bsobj 因为如果缩小范围可能找不到

                str_content = 'content' + '\n'+ contend.get_text() + '\n'
                f_blog.write(str_content)

        f_blog.close()

        response.close()  # 注意关闭response
    except OSError as e:
        print(e)
    except urllib.error.URLError as e:
        print(e.reason)
    except Exception as e:
        print(e)


#
def getPage_AllBlogLinks(url,url_pattern):
    try:
        randdom_header = random.choice(my_headers)

        req = urllib.request.Request(url)

        req.add_header("User-Agent", randdom_header)
        req.add_header("GET", url)

        response = urllib.request.urlopen(req)
    # html = response.read().decode('utf-8')
    #     # print(html)
        page_content = response.read()
        bsObj = BeautifulSoup(page_content, "html.parser")
        etree_obj = etree.HTML(page_content)
    # 获取文章的文字内容
    # 获取网页信息
    #此处逻辑应为：首先获取文章box 的id 之后获取，title 的，之后是content 的
    # 将每一篇博客分别保存为一个文件

        list_blog_obj = []

        list_page_title = bsObj.findAll(name='div', attrs={'class': 'article-item-box csdn-tracking-statistics'})
        page_link_pattern = "(" + url_pattern + ")"

        for page_obj in list_page_title:
            page_link = page_obj.findAll(name='a')[0].attrs['href']
            if re.match(page_link_pattern,page_link):
                id = page_link.split('/')[-1]
                create_time =page_obj.findAll(name='div')[0].findAll(name='span')[0].get_text()
                click_number =page_obj.findAll(name='div')[0].findAll(name='span')[1].get_text().replace('阅读数：','')
                comment_number =page_obj.findAll(name='div')[0].findAll(name='span')[2].get_text().replace('评论数：','')

                temp_blog = CSDN_Blog.CSDN_Blog(id=id, name='', contend='', create_time=create_time, click_number=click_number, comment_number=comment_number,label='')
                #构造类的对象，
                list_blog_obj.append(temp_blog)
            else:
                pass
        response.close()  # 注意关闭response
        return list_blog_obj

    except OSError as e:
        print(e)
    except urllib.error.URLError as e:
        print(e.reason)
    except Exception as e:
        print(e)


#先获取所有博客的id 和链接，然后按照链接依次爬取
def main():
    from Database import  CSDN_Blog
    # 得到CSDN博客某一个分页的所有文章的链接
    #CSDN_Blog(id='', name='', contend='', create_time='', click_number='', comment_number='',label='')
    #CSDN_Blog()
    articles = set()

    # 得到CSDN博客某个博客主页上所有分页的链接，根据分页链接得到每一篇文章的链接并爬取博客每篇文章的文字
    pages = set()
    ####获取到每一个分页列表的所有文章
    str_page_url_prefix = 'https://blog.csdn.net/wangyaninglm/'

    list_page_str = str_page_url_prefix + 'article/list/'

    list_blog_obj = []

    # 获取分页数量, 由于这部分分页代码为自动生成 ，所以需要使用 selenium，如果觉的麻烦可以直接把分页数量作为输入

    # import spider_selenium
    # page_index = spider_selenium.get_csdn_page_index(str_page_url_prefix,'ui-pager')
    page_index = 17
    # 输入分页数据量
    for i in range(1, page_index + 1):
        # print(list_page_str + str(i))
        temp_blog_obj = getPage_AllBlogLinks((list_page_str + str(i)),str_page_url_prefix)
        list_blog_obj.extend(temp_blog_obj)

    page_url_list = []
    page_url_pattern = "(" + str_page_url_prefix + "article/details)(/[0-9]+)*$"

    for page_link in articles:

        if re.match(page_url_pattern, page_link):
            page_url_list.append(page_link)
        else:
            pass

    print(len(page_url_list))

    dict_page_content = {'title': '', 'content': ''}
    list_page_content = []

    for url in page_url_list:
        get_Content(url, 'blog-content-box', 'title-article', 'article_content')


if __name__ == '__main__':
    main()

#所有内容class：blog-content-box 标题class：title-article， 内容id： article_content


#需要改进的地方：title 中存在重复，
# 报错：EOF occurred in violation of protocol (_ssl.c:777)

