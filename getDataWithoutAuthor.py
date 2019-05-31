'''
@返回数据格式:
[{
		'firstFloorContent': '第一楼内容',
		'title': '标题',
		'href': 'http链接',
		'positive_prob': 积极性,
		'confidence': 可信度
	},

	{
		'firstFloorContent': '第一楼内容',
		'title': '标题',
		'href': 'http链接',
		'positive_prob': 积极性,
		'confidence': 可信度
	}
]

'''


from tiebaSpider import spiderOnlyFirstFloorAdvance as soffa
from SentimentAnalysis import Analysis
import csv
import time

def getContentAndSentimentDict(page=1, keyword="杭州电子科技大学"):
	articleList = soffa.gogogo_list_first_floor_advance(page, keyword)
	# 获取所有文章的信息的列表，每个数据元素格式如下

	'''
	{'authorName': '作者', 
	'firstFloorContent': '第一楼内容', 
	'title': '标题', 
	'href': 'http链接'}
	'''
	for article in articleList:
		sentimentDict = Analysis.analysisDict(article['firstFloorContent'])
		# 对每篇文章第一楼内容进行情感分析
		article['positive_prob'] = sentimentDict['items'][0]['positive_prob']
		# 积极性存回字典
		article['confidence'] = sentimentDict['items'][0]['confidence']
		# 积极性存回字典
		# print(article)
	return articleList

def getContentAndSentimentDictToCsv(page=1, keyword="杭州电子科技大学"):
	headers = ['authorName', 'firstFloorContent', 
				'title', 'href', 'positive_prob', 'confidence']
	dataList = getContentAndSentimentDict(page = page, keyword = keyword)
	print("All contents with sentiment done")
	dateTime = time.strftime("%Y-%m-%d_%H_%M", time.localtime())
	# 按时间存储
	fileName = 'data\\'+dateTime+'_'+keyword.replace(' ','_')+'.csv'
	# 拼接文件名，并且将关键词中的空格替换为下划线
	with open(fileName, 'w') as f:
		print('saving '+fileName)
		dWriter = csv.DictWriter(f, dataList[0].keys())
		# 用键列表定义csv写对象
		dWriter.writeheader()
		# 写列名
		for data in dataList:
			dWriter.writerow(data)
		print('save done')




if __name__ == '__main__':
	print("start")
	page = 1
	keyword = "杭州电子科技大学 三位一体"
	'''
	dataList = getContentAndSentimentDict(page = page, keyword = keyword)
	# print(dataList)
	print("All contents with sentiment done")
	for data in dataList:
		print(data)
	'''

	getContentAndSentimentDictToCsv(page=page, keyword = keyword)
