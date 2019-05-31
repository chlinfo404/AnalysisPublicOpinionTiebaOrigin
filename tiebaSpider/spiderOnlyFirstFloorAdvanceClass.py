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
from urllib.parse import quote

class TiebaCrawl:
	headers = {
				'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
				}
	urlPrefix = "http://tieba.baidu.com/f/search/res?ie=utf-8&isnew=1&kw=&qw="
	urlSuffix = "&un=&rn=10&pn=0&sd=&ed=&sm=1&only_thread=1&pn="

	def __init__(self, keyWord = "杭州电子科技大学"):
		self.result = []
		self.keyWord = keyWord

	def pause(self):
		'''
		延迟一到两秒
		'''
		sleepTime = random.randint(100,500)*1.0/1000
		# 延迟0.1-0.5秒
		time.sleep(sleepTime)

	def make_up_url(self):
		'''
		组装url
		urlPrefix:前缀
		urlPrefix:后缀
		keyWord:关键词
		'''
		return self.urlPrefix + quote(self.keyWord) + self.urlSuffix
		# 网址用的是百分号编码

	def get_url_list_of_one_page(self, originUrl, page = 0):
		'''
		获取某页所有的链接
		originUrl: 得到的网址
		page: 页数
		'''

		# global originUrl
		# url = originUrl + str(page*50)
		# 拼装每一页实际网址并请求
		# 这是1.0请求网页的网址
		url = originUrl +str(page + 1)
		content = requests.get(url, headers = self.headers)
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

	def get_soup_of_article(self, articleUrl, page=1):
		'''
		获取每一页soup对象
		'''
		url =  articleUrl + "?pn="
		htmlText = requests.get(url+str(page), headers=self.headers)
		soup = BeautifulSoup(htmlText.text, 'lxml')
		return soup

	def get_title(self, article):
		'''
		获取标题
		随便哪页都能获取，选第一页
		'''
		soup = self.get_soup_of_article(article, 1)
		title = soup.find(class_='core_title_txt')['title'].strip()
		return title

	def get_main_content_first_floor_advance(self, articleSoup):
		# 返回列表
		contentDistrict = articleSoup.find(class_="d_post_content_firstfloor")
		# 因为是第一楼这样子定位更精确更快
		content = contentDistrict.find(class_=['d_post_content','j_d_post_content'])
		# 获得内容
		if(content != None):
			content = content.text.strip()
		else:
			content = ""
		self.pause()

		return content

	def gogogo_list_first_floor_advance(self, pageWant = 1, keyWord = "杭州电子科技大学"):
		'''
		根据关键词和指定页数爬取
		pageWant:爬搜索结果的几页
		keyWord:关键词
		'''
		originUrl = self.make_up_url()
		for page in range(pageWant):	# 逐页爬取
			articleList = self.get_url_list_of_one_page(originUrl, page)
			for article in articleList:
				soup = self.get_soup_of_article(article)
				title = self.get_title(article)
				oneArticleDict = {}
				oneArticleDict['firstFloorContent'] = self.get_main_content_first_floor_advance(soup)
				oneArticleDict['title'] = title
				oneArticleDict['href'] = article
				# print(oneArticleDict)
				self.result.append(oneArticleDict)
			print("page", page+1, "done")

		print("All firstFloorContent done")
		return self.result

if __name__ == '__main__':

	start_time = time.time()
	print('开始爬取')
	tc = TiebaCrawl()
	result = tc.gogogo_list_first_floor_advance(3, "杭州电子科技大学 三位一体")
	print(result)
	end_time = time.time()
	print("time used %f s" % (end_time - start_time))