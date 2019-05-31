#!/user/bin/python
# -*- coding: utf-8 -*-
from BaseReptile import BaseReptile
import time
import random


class Proxy(object):
    def __init__(self, url):
        self.url = url
        self.proxy = None
        self.__proxy_times = 0

    def get_proxy(self):
        """
        代理ip和本机ip轮换
        :return:
        """
        if self.__proxy_times == 0:
            self.proxy = self.request_proxy()
            self.__proxy_times = 1
        else:
            self.proxy = None
            self.__proxy_times = 0
            print("local mode")
        return self.proxy

    def request_proxy(self):
        """
        获取代理ip
        :return:
        """
        while True:
            try:
                s = str(BaseReptile(self.url).get_html_text())
                proxies = {"http": "%s" %s}
                print("开始请求代理 ")
                print(proxies)
                baseReptile = BaseReptile("http://cnki.net/")
                baseReptile.get_response(proxies=proxies, timeout=5)
                if len(s.split(":")) == 2 and baseReptile.requestCode == 1:
                    print("开启代理 %s" % s)
                    return proxies
                else:
                    print("再次请求代理")
            except:
                print("代理无效，再次请求代理")
                time.sleep(random.randint(1, 4))


if __name__ == '__main__':
    proxy = Proxy("http://tpv.daxiangdaili.com/ip/?tid=557133875098914&num=1&delay=5&filter=on")
    proxy.get_proxy()
