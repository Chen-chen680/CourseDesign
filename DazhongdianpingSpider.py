import random
import time
import re
import requests
from pyquery import PyQuery as pq
import webbrowser

COOKIES = 'fspop=test; _lxsdk_cuid=179eab48f92c8-00d7d2ecbe7ea8-d7e1938-144000-179eab48f92e; _lxsdk=179eab48f92c8-00d7d2ecbe7ea8-d7e1938-144000-179eab48f92e; _hc.v=2d4c0ba6-3ce4-3179-3236-7b581f60667e.1623140373; s_ViewType=10; cy=2; cye=beijing; _dp.ac.v=042ee016-92c2-4218-bee9-1cbc41fdbd4c; ua=dpuser_2111661415; ctu=cdafd198fbd0dcc3431635a635cd1ea8b288af5c6bc11f29a5ae976db2f89f6e; aburl=1; dplet=0220ed74be6edea8f793a8bfba17d7bb; dper=f58a4b6a5133da50e25aba61a1b1a9fdd72de69c353683265cbdf024529f7c4efe4968ce62014a3ab65e037bd646e557212d9452737c4f462f8bab48bf19d681dd3b69ec679eab54937c87ab0a51527baa2233ce8280d60e09d296c573d9d9ed; ll=7fd06e815b796be3df069dec7836c3df; _lx_utm=utm_source=Baidu&utm_medium=organic; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1623310304,1623315523,1623393058,1623393072; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1623393075; _lxsdk_s=179f9c43b20-8dd-dd6-388||48'
f = open('测试.txt', 'w',encoding='utf-8')
font_size = 14
start_y = 23
ii = 0
class DianpingComment():
    '''
    大众点评css解密思路：
    第一个一行中，字体的位置 (/ 14) 从零开始， 第二个加23就是其id对应的位置
    '''
    COOKIES = 'fspop=test; _lxsdk_cuid=179eab48f92c8-00d7d2ecbe7ea8-d7e1938-144000-179eab48f92e; _lxsdk=179eab48f92c8-00d7d2ecbe7ea8-d7e1938-144000-179eab48f92e; _hc.v=2d4c0ba6-3ce4-3179-3236-7b581f60667e.1623140373; s_ViewType=10; cy=2; cye=beijing; _dp.ac.v=042ee016-92c2-4218-bee9-1cbc41fdbd4c; ua=dpuser_2111661415; ctu=cdafd198fbd0dcc3431635a635cd1ea8b288af5c6bc11f29a5ae976db2f89f6e; aburl=1; dplet=0220ed74be6edea8f793a8bfba17d7bb; dper=f58a4b6a5133da50e25aba61a1b1a9fdd72de69c353683265cbdf024529f7c4efe4968ce62014a3ab65e037bd646e557212d9452737c4f462f8bab48bf19d681dd3b69ec679eab54937c87ab0a51527baa2233ce8280d60e09d296c573d9d9ed; ll=7fd06e815b796be3df069dec7836c3df; _lx_utm=utm_source=Baidu&utm_medium=organic; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1623310304,1623315523,1623393058,1623393072; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1623393075; _lxsdk_s=179f9c43b20-8dd-dd6-388||48'
    f = open('测试.txt', 'w', encoding='utf-8')
    font_size = 14
    start_y = 23
    ii = 0
    def __init__(self, shop_id, cookies, delay=7):
        '''
        :param shop_id: 页面的id
        :param cookies: 你的个人cookie
        :param delay: 延迟参数
        '''
        self.shop_id = shop_id
        if delay < 2:
            self._delay = 23
        else:
            self._delay = delay
        self.num = 1
        self._cookies = self._format_cookies(cookies)
        self.page = 1
        self.end_page = 572
        self.data_num = 1
        self._css_headers = {
            'Host': 's3plus.meituan.net',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
        }

        self._default_headers = {
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
        self._cur_request_url = 'http://www.dianping.com/shop/{}/review_all'.format(self.shop_id) # 得到页面idw
        webbrowser.open(self._cur_request_url)
        self.origin_url = self._cur_request_url
        self.sub_url = 'http://www.dianping.com'

    def _delay_func(self):
        '''随机延时函数'''
        delay_time = random.randint((self._delay - 2), (self._delay + 2))
        time.sleep(delay_time)

    def _format_cookies(self, cookies):
        '''
        获取cookies;;;
        '''
        cookies = {cookie.split('=')[0]: cookie.split('=')[1]
                   for cookie in cookies.replace(' ', '').split(';')}
        return cookies

    def _get_conment_page(self):
        """
            请求评论页，并将<span></span>样式替换成文字;
        """
        self._cur_request_url = 'http://www.dianping.com/shop/G3Do5L1eWZVQvRyb/review_all/p1'
        self.page = 1

        while self._cur_request_url:
            self._delay_func()
            res = requests.get(self._cur_request_url, headers=self._default_headers, cookies=self._cookies)
            while res.status_code != 200:
                cookie = random.choice(COOKIES)
                cookies = self._format_cookies(cookie)
                res = requests.get(self._cur_request_url, headers=self._default_headers, cookies=cookies)
                if res.status_code == 200:
                    break
            html = res.text
            class_set = []
            for span in re.findall(r'<svgmtsi class="([a-zA-Z0-9]{5,6})"></svgmtsi>', html):
                class_set.append(span)
            for class_name in class_set:
                try:
                    html = re.sub('<svgmtsi class="%s"></svgmtsi>' % class_name, self._font_dict[class_name], html)
                except:
                    html = re.sub('<svgmtsi class="%s"></svgmtsi>' % class_name, '', html)
            doc = pq(html)
            self._parse_comment_page(html)  # 解析网页
            self.page += 1
            self._cur_request_url = self.origin_url + '/p' + str(self.page)
            next_page_url = self._cur_request_url
            print('next_page_url:{}'.format(next_page_url))
            time.sleep(3)
            if self.page > self.end_page:
                break

    def _parse_comment_page(self, html):
        """
            解析评论页并提取数据,把数据写入文件中；；
        """
        doc = pq(html)
        for li in doc('div.review-list-main > div.reviews-wrapper > div.reviews-items > ul > li'):

            doc_text = pq(li)
            if doc_text('.dper-info .name').text():
                name = doc_text('.dper-info .name').text()
            else:
                name = None
            try:
                star = doc_text('.review-rank .sml-rank-stars').attr('class')
            except IndexError:
                star = None
            if doc_text('div.misc-info.clearfix > .time').text():
                date_time = doc_text('div.misc-info.clearfix > .time').text()
            else:
                date_time = None

            if doc_text('.main-review .review-words').text():
                comment = doc_text('.main-review .review-words').text().replace(r'\n收起评价', '')
            else:
                comment = None
            data = {
                'name': name,
                'date_time': date_time,
                'star': star,
                'comment': comment
            }
            print(self.data_num, data)
            self.data_num += 1
            if len(data) == 0:
                webbrowser.open(self._cur_request_url) # 若请求失败，使用浏览器输入验证码，在继续请求
                time.sleep(30)
            f.write(str(data))
            f.write("\n") # 写入，显示数据

    def _get_css_link(self, url):
        """
            请求评论首页，获取css样式文件
        """
        try:
            res = requests.get(url, headers=self._default_headers, cookies=self._cookies)
            html = res.text
            css_link = re.search(r'<link re.*?css.*?href="(.*?svgtextcss.*?)">', html)
            assert css_link
            css_link = 'http:' + css_link[1]
            return css_link
        except:
            pass

    def _get_font_dict(self, url):
        """
            获取css样式对应文字的字典
        """
        res = requests.get(url, headers=self._css_headers)
        html = res.text
        background_image_link = re.findall(r'background-image:.*?\((.*?svg)\)', html)
        background_image_link_list = []
        for i in background_image_link:
            url = 'http:' + i
            background_image_link_list.append(url)
        html = re.sub(r'span.*?\}', '', html)
        group_offset_list = re.findall(r'\.([a-zA-Z0-9]{5,6}).*?round:(.*?)px (.*?)px;', html)
        '''
        多个偏移字典，合并在一起；；；
        '''
        font_dict_by_offset_list = {}
        for i in background_image_link_list:
            font_dict_by_offset_list.update(self._get_font_dict_by_offset(i))
        font_dict_by_offset = font_dict_by_offset_list
        font_dict = {}
        for class_name, x_offset, y_offset in group_offset_list:
            x_offset = x_offset.replace('.0', '')
            y_offset = y_offset.replace('.0', '')
            try:
                font_dict[class_name] = font_dict_by_offset[int(y_offset)][int(x_offset)]
            except:
                font_dict[class_name] = ''
        return font_dict

    def _get_font_dict_by_offset(self, url):
        """
            获取坐标偏移的文字字典, 会有最少两种形式的svg文件（目前只遇到两种）
        """
        res = requests.get(url, headers=self._css_headers)
        html = res.text
        font_dict = {}
        y_list = re.findall(r'd="M0 (\d+?) ', html)
        if y_list:
            font_list = re.findall(r'<textPath .*?>(.*?)<', html)
            for i, string in enumerate(font_list):
                y_offset = self.start_y - int(y_list[i])

                sub_font_dict = {}
                for j, font in enumerate(string):
                    x_offset = -j * self.font_size
                    sub_font_dict[x_offset] = font
                font_dict[y_offset] = sub_font_dict
        else:
            font_list = re.findall(r'<text.*?y="(.*?)">(.*?)<', html)
            for y, string in font_list:
                y_offset = self.start_y - int(y)
                sub_font_dict = {}
                for j, font in enumerate(string):
                    x_offset = -j * self.font_size
                    sub_font_dict[x_offset] = font
                font_dict[y_offset] = sub_font_dict
        return font_dict

    def run(self):
        self._css_link = self._get_css_link(self._cur_request_url) #得到css链接
        self._font_dict = self._get_font_dict(self._css_link) #得到解密的字典
        self._get_conment_page() #开始爬虫

if __name__ == "__main__":
    dianping = DianpingComment('G3Do5L1eWZVQvRyb', cookies=COOKIES)  #
    dianping.run()
    f.close()
