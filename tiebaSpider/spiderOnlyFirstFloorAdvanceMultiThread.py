"""
@author:BirdBirdLee
@time:2019/03/08
@note:应老师要求，只爬第一楼，并做情感分析，所以对传回字典进行格式修改
"""

from bs4 import BeautifulSoup
import requests
import re
import time
import random
import json
import time
import threading
from queue import Queue
from urllib.parse import quote
from Proxy import Proxy

headers = {
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
		}

proxy = Proxy("http://tpv.daxiangdaili.com/ip/?tid=557133875098914&num=1&delay=5&filter=on")
proxies = None

def get_proxy():
	global proxy
	return proxy.get_proxy()

def pause():
	'''
	延迟一到两秒
	'''
	sleepTime = random.randint(100,200)*1.0/1000
	# 延迟0.1-0.2秒
	time.sleep(sleepTime)

def make_up_url(urlPrefix, urlSuffix, keyWord):
	'''
	组装url
	urlPrefix:前缀
	urlPrefix:后缀
	keyWord:关键词
	'''
	return urlPrefix + quote(keyWord) + urlSuffix
	# 网址用的是百分号编码

def get_url_list_of_one_page(originUrl, page = 0):
	'''
	获取某页所有的链接
	originUrl: 得到的网址
	page: 页数
	'''

	# global originUrl
	# url = originUrl + str(page*50)
	# 拼装每一页实际网址并请求
	# 这是1.0请求网页的网址
	global proxies
	proxies = get_proxy()
	url = originUrl +str(page + 1)
	content = requests.get(url, headers = headers, proxies = proxies)
	pattern = r'href="(/p/[0-9]*)[^ ]'
	# 获取每一页上所有文章的网址
	articleList = re.findall(pattern, content.text)

	'''
	for article in articleList:
		article = "http://tieba.baidu.com"+article
		print(article)
	'''
	# 这种形式无法改变列表的值

	for i in range(len(articleList)):
		articleList[i] = "http://tieba.baidu.com" + articleList[i]
	return articleList

def get_soup_of_article(articleUrl, page=1):
	'''
	获取每一页soup对象
	'''
	global proxies
	proxies = get_proxy()
	url =  articleUrl + "?pn="
	htmlText = requests.get(url+str(page), headers=headers, proxies=proxies)
	soup = BeautifulSoup(htmlText.text, 'lxml')
	return soup

def get_title(article):
	'''
	获取标题
	随便哪页都能获取，选第一页
	'''
	soup = get_soup_of_article(article, 1)
	title = soup.find(class_='core_title_txt')['title'].strip()
	return title

def get_main_content_first_floor_advance(articleSoup):
	# 返回列表
	contentDistrict = articleSoup.find(class_="d_post_content_firstfloor")
	# 因为是第一楼这样子定位更精确更快
	content = contentDistrict.find(class_=['d_post_content','j_d_post_content'])
	# 获得内容
	if(content != None):
		content = content.text.strip()
	else:
		content = ""
	pause()

	return content

def gogogo_list_first_floor_advance(pageWant = 1, keyWord = "杭州电子科技大学"):
	'''
	根据关键词和指定页数爬取
	pageWant:爬搜索结果的几页
	keyWord:关键词
	'''
	result = []
	urlPrefix = "http://tieba.baidu.com/f/search/res?ie=utf-8&isnew=1&kw=&qw="
	urlSuffix = "&un=&rn=10&pn=0&sd=&ed=&sm=1&only_thread=1&pn="
	originUrl = make_up_url(urlPrefix, urlSuffix, keyWord)
	for page in range(pageWant):	# 逐页爬取
		articleList = get_url_list_of_one_page(originUrl, page)
		for article in articleList:
			soup = get_soup_of_article(article)
			title = get_title(article)
			oneArticleDict = {}
			oneArticleDict['firstFloorContent'] = get_main_content_first_floor_advance(soup)
			oneArticleDict['title'] = title
			oneArticleDict['href'] = article
			# print(oneArticleDict)
			result.append(oneArticleDict)
		print("page", page+1, "done")

	print("All firstFloorContent done")
	return result

if __name__ == '__main__':

	start = time.time()
	print('开始爬取')
	'''
	for t in threads:
		t.setDaemon(True)
		t.start()

	t.join()
	'''
	result = gogogo_list_first_floor_advance(3, "杭州电子科技大学 三位一体")
	end = time.time()
	print("time used:",end-start)
	# print(result)
	print(len(result))