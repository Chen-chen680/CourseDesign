import requests
import json
import re
import time

class BaiduNlp(object):
    def __init__(self):
        # 申请的API接口信息
        self.ak = ''
        self.sk = ''
        self.app_id = ''

        self.header = {'Content-Type': 'application/json'}
        self.comment_extract_url = 'https://aip.baidubce.com/rpc/2.0/nlp/v2/comment_tag?charset=UTF-8&access_token='
        self.sentiment_url = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify?charset=UTF-8&access_token='
        self._GetAccessToken()
        self._readData()
        self.star_partern = 'sml-rank-stars sml-str(\d+) star'

    def _GetAccessToken(self):
        '''得到请求的Access Token'''
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s' % (self.ak , self.sk)
        response = requests.get(host).json()
        self.access_token = response['access_token']

    def _readData(self):
        '''读取爬取的数据'''
        datas = open(r'泰山大众点评.txt', 'r', encoding='utf8').readlines()
        for index, data in enumerate(datas):
            datas[index] = eval(data)
        self.data = datas

    def CommentExtract(self):
        url = self.comment_extract_url + self.access_token
        data = {
            "text": "这里的风景真的太好了",
            "type": 5
        }
        data = json.dumps(data)
        response = requests.post(url=url, data=data, headers=self.header).json()
        from pprint import pprint
        pprint(response)

    def Sentiment(self):
        file = open('SentimentAnalysis1.csv', 'w', encoding='utf-8_sig')
        file.write('用户,评分,评论时间,积极分数,消极分数,置信度\n')
        '''进行情感分析'''
        url = self.sentiment_url + self.access_token # 得到请求api的url
        i = 0
        for one_user in self.data:
            i+= 1
            # 取出数据
            user_name = one_user['name']
            data_time = one_user["date_time"]
            star = re.findall(self.star_partern, one_user['star'])[0]
            comment = one_user['comment']
            if len(comment) > 1023:
                comment = comment[0: 1023]
            # 发送的数据
            data = {
                'text': comment
            }
            data = json.dumps(data)
            response = requests.post(url=url, data=data, headers=self.header).json() # 进行请求，返回数据
            while 'error_code' in response.keys(): # 判断是否出错
                time.sleep(5)
                response = requests.post(url=url, data=data, headers=self.header).json()
            result = response['items'][0] # positive_prob：积极分数; confidence：置信度; negative_prob：消极分数; sentiment：情感分类
            positive, negative, confidence = str(result['positive_prob']), str(result['negative_prob']), str(result['confidence'])
            file.write("%s,%s,%s,%s,%s,%s\n" % (user_name, star, data_time, positive, negative, confidence))
            print(i, "%s,%s,%s,%s,%s,%s\n" % (user_name, star, data_time, positive, negative, confidence))
            time.sleep(0.2)

if __name__ == '__main__':
    a = BaiduNlp()
    a.Sentiment()