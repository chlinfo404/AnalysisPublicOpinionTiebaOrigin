#!/user/bin/python
# -*- coding: utf-8 -*-
import requests
from lxml import etree


class BaseReptile(object):
    """
    解析一个网页的基本类（解析网页的基本方法）
    """
    def __init__(self, url=None):
        self.url = url
        self.html = None
        self.response = None
        self.html_content = None
        self.tree = None
        self.requestCode = -1  # 表示请求返回的结果，-1代表还未请求或服务器不给于请求相应，0代表请求地址不存在，1代表请求成功

    def init(self, model="get", params=None, **kwargs):
        self.get_etree(model, params, **kwargs)

    def reset(self, url, model="get", params=None, **kwargs):
        self.get_etree(model, params, **kwargs)

    def get_url(self):
        return self.url

    def set_url(self, url):
        self.url = url

    def is_response(self, response):
        """
        判断是否得到正确的请求响应，爬取不同的网页可能需要继承修改
        :param response: 
        :return: 
        """
        if response and response.status_code == 200 and response.url == self.url:
            return True
        else:
            print(response.url)
            return False

    def get_response(self, model="get", params=None, **kwargs):
        """
        根据请求方式获取请求的response
        :param model: 
        :param params: 
        :param kwargs: 
        :return: 
        """
        try:
            if model == "post":
                self.response = requests.post(self.url, params, **kwargs)
            else:
                self.response = requests.get(self.url, params, **kwargs)
            if self.is_response(self.response):
                self.requestCode = 1
                return self.response
            else:
                self.requestCode = 0
                print("网页请求不存在！")
                return None
        except Exception as e:
            self.requestCode = -1
            print("获取网页内容失败！")
            return None

    def get_html_text(self, model="get", params=None, **kwargs):
        """
        获得网页html内容
        :param model: 
        :param params: 
        :param kwargs: 
        :return: 
        """
        response = self.get_response(model, params, **kwargs)
        if response:
            self.html = response.text
        else:
            self.html = None
        return self.html

    def get_html_content(self, model="get", params=None, **kwargs):
        """
        获得网页html内容(二进制内容，下载文件的时候需要用到)
        :param model: 
        :param params: 
        :param kwargs: 
        :return: 
        """
        response = self.get_response(model, params, **kwargs)
        if response:
            self.html_content = response.content
        else:
            self.html = None
        return self.htmlContent

    def get_etree(self, model="get", params=None, **kwargs):
        """
        将html的页面形成一个文档树，主要是调用etree.HTML这个方法
        :param model: 
        :param params: 
        :param kwargs: 
        :return: 
        """
        self.get_html_text(model, params, **kwargs)
        if self.html:
            self.tree = etree.HTML(self.html)
        else:
            self.tree = None
        return self.tree

    # def get_elements_text(self, regex, index=0):
    #     """
    #     得到网页中某元素固定位置的文本值
    #     :param regex:
    #     :param index:
    #     :return:
    #     """
    #     elements = self.get_elements(regex)
    #     if elements and len(elements) > index:
    #         return elements[index].text
    #     else:
    #         return None
    #
    # def get_all_elements_text(self, regex):
    #     """
    #     得到符合正则表达式的所有元素的文本
    #     :param regex:
    #     :return: a List
    #     """
    #     elements = self.get_elements(regex)
    #     if elements:
    #         return [n.text for n in elements]
    #     else:
    #         return None

    # def get_elements(self, regex):
    #     """
    #     得到网页中某元素
    #     :param regex:
    #     :return:
    #     """
    #     return self.tree.xpath(regex)

    def index_of_elements_info(self, regex, index=0):
        elements = self.get_elements_info(regex)
        if elements and len(elements) > index:
            return elements[index]
        return None

    def get_elements_info(self, regex):
        """
        得到网页中某元素
        :param regex: 
        :return: 
        """
        elements = self.tree.xpath(regex)
        if elements:
            return elements
        else:
            return None

    def list_to_str(self, list, separator=""):
        if list:
            return separator.join([n.strip() for n in list])
        else:
            return None

    def parse_html(self):
        """
        解析网页内容，继承需要重写
        :return: 
        """
        raise RuntimeError("no complete this function")

