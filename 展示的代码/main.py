import requests
from lxml import etree
import json
import re
import webbrowser
import time

'''
大众点评css解密思路：
第一个一行中，字体的位置 (/ 14) 从零开始， 第二个加23就是其id对应的位置

origin    svg
1037      1060
81        104
257       280

//s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/49e7db807989712de032fac5a40b73e1.svg
//s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/3335495deda3c78f3ab47311e115dac5.svg
//s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/fee0f08fbc2b132bafb87d3daa057cd8.svg
coment: xpath : //div[@class="review-truncated-words"]
'''

class Spider():
    def __init__(self, url):
        self.header_css = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Host': 's3plus.meituan.net',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36'
        }

        self.header = {
            'Referer': 'http://www.dianping.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36'
        }
        self.url = url
        self.response_main = None

    def request(self):
        self.response_main = requests.get(self.url, headers=self.header) # 请求评论主网页，如：http://www.dianping.com/shop/G1Wk8Pk8LyS8IjIe/review_all
        html = etree.HTML(self.response_main.text)
        try:
            css_url = html.xpath('/html/head/link[4]/@href')[0]
        except:
            webbrowser.open(self.url)
            time.sleep(20)
        css_url = 'http:' + css_url  # 得到css网址
        response = requests.get(css_url, headers=self.header_css)
        reg = 'background-image: url\((.*?)\)'
        url = re.findall(reg, response.text)  # 得到svg地址
        url = 'http:' + url[2]
        self.svg_response = requests.get(url, headers=self.header_css) # svg请求

    def parse(self):
        if self.response_main == None:
            self.request()
        xpath_comment = '//div[@class="reviews-items"]/ul/li'
        main_html = etree.HTML(self.response_main.text)
        comments = main_html.xpath(xpath_comment)

        for index in range(len(comments)):
            one_word_element = main_html.xpath(xpath_comment + '[' + str(index + 1) + ']' + '//div[@class="review-truncated-words"]')
            one_comment_html = etree.tostring(one_word_element[0], encoding = "utf-8").decode('utf-8')
            print('\n')
            print(one_comment_html)

if __name__ == '__main__':
    a = Spider(url='http://www.dianping.com/shop/G1Wk8Pk8LyS8IjIe/review_all')
    a.parse()