import requests
from lxml import etree
import time
import webbrowser
import re
import json

class QuNaer():
    def __init__(self,
                 url):
        self.url = url
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36'}
        self.api_url = 'http://travel.qunar.com/place/api/html/comments/poi/{}?poiList=true&sortField=1&rank=0&pageSize=10&page='
        self.User_api_url = 'http://travel.qunar.com/place/api/comments/{}/replies?page=1&pageSize=10&format=json'
        self.Comment_NUm_xpath = "//a[@id='more_cmt_href']/text()"
        self.TOTAL_PAGE_xpath = '//*[@id="js_replace_box"]/div[2]/div/a[7]/text()'
        self.USER_URL_xpath = '//a[@class="seeMore"]/@href'
        self.current_page = 1
        self.TOTAL_PAGE = None # 总的页数
        self.Total_COMMENT = None
        self.TotalPageGet()
        self.Ulr_get()

    def TotalPageGet(self):
        response = self.Requests(self.url)
        html = response.text
        html = etree.HTML(html)
        comment_num = html.xpath(self.Comment_NUm_xpath)[0]
        page = int(html.xpath(self.TOTAL_PAGE_xpath)[0])
        comment_num = eval(re.findall(r'共(\d+)条点评', comment_num)[0])
        self.TOTAL_PAGE, self.Total_COMMENT = page, comment_num
        print("共{}页，{}条评论".format(self.TOTAL_PAGE, self.Total_COMMENT))

    def TimeTransform(self, createTime):
        createTime = str(createTime)
        createTime1 = createTime[0:-3]
        createTime2 = createTime[-3: len(createTime)]
        createTime = createTime1 + '.' + createTime2
        createTime = float(createTime)
        createTime = time.localtime(createTime)
        createTime = time.strftime('%Y-%m-%d %H:%M:%S', createTime)
        return createTime

    def Requests(self, url):
        response = requests.get(url, headers = self.headers)
        time.sleep(1)
        if response.status_code == 200:
            return response
        else:
            webbrowser.open(self.url)
            time.sleep(30)
            self.Requests(url)

    def OnePageProcess(self, response, file):
        html = response.text
        html = json.loads(html)
        if html['success'] != True:
            print('--------------------请求失败------------------')
            return
        else:
            data = html['data']
            data = etree.HTML(data)
            SeeMore_list = data.xpath(self.USER_URL_xpath)
            for one_user_url in SeeMore_list:
                user_poi = ''.join([x for x in one_user_url if x.isdigit()])
                one_user_url = self.User_api_url.format(user_poi)
                response = self.Requests(one_user_url)
                data = response.json()
                if len(data) == 0:
                    continue
                if data['errmsg'] != 'success':
                    print('-----------请求失败-------')
                    continue
                data = data['data']['json']
                result_dict = {}
                if len(data) != 0:
                    try:
                        createTime = data[0]['parentComment']['createTime']
                        createTime = self.TimeTransform(createTime)
                        comment = data[0]['parentComment']['body']
                        user = data[0]['owner']['nickName']

                        result_dict['user'] = user
                        result_dict['createTime'] = createTime
                        result_dict['comment'] = comment
                        result_dict = str(result_dict)
                        print(user, createTime)
                        file.write(result_dict + '\n')
                    except:
                        continue

    def Ulr_get(self):
        ''''''
        file = open('去哪儿网爬虫.txt', 'w', encoding='utf8')
        self.poi = ''.join([x for x in self.url if x.isdigit()])
        self.api_url = self.api_url.format(self.poi)
        for index in range(1, self.TOTAL_PAGE + 1):
            url = self.api_url + str(index)
            response = self.Requests(url)
            if response.status_code != 200:
                continue
            else:
                self.OnePageProcess(response, file)

if __name__ == '__main__':
    obj = QuNaer(r'http://travel.qunar.com/p-oi709762-mogaoku')
