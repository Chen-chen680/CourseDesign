import requests
import re
from lxml import etree

ALL_PAGE = 7

def Parse(response, f):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36'}
    day_url_xpath = '//div[@class="contMain fontSt"]/ul/li/a/@href'
    html = response.content.decode('utf8')
    html_etree = etree.HTML(html)
    reg_data = r'截至(\d+)月(\d+)日(\d+)时，全省累计报告新型冠状病毒肺炎确诊病例(\d+)例\(其中境外输入(\d+)例\），累计治愈出院(\d+)例，死亡(\d+)例，目前在院隔离治疗(\d+)例，(\d+)人尚在接受医学观察。'
    url_list = html_etree.xpath(day_url_xpath)
    for url in url_list:
        url = 'http://wsjkw.sc.gov.cn' + url
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise RuntimeError('请求失败')
        html = response.content.decode('utf8')
        result = re.findall(reg_data, html)
        result = result[0]
        print(result[0] + '月' + result[1] + '日' + result[2] + '时' + ',' + result[3] + ',' + result[4] + ',' + result[5] + ',' + result[6] + ',' + result[7] + ',' + result[8] + '\n')
        f.write(result[0] + '月' + result[1] + '日' + result[2] + '时' + ',' + result[3] + ',' + result[4] + ',' + result[5] + ',' + result[6] + ',' + result[7] + ',' + result[8] + '\n')

def CovidSichuan():

    HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36'}
    url = 'http://wsjkw.sc.gov.cn/scwsjkw/gzbd01/ztwzlmgl.shtml'
    url1 = 'http://wsjkw.sc.gov.cn/scwsjkw/gzbd01/ztwzlmgl_'
    response = requests.get(url=url, headers=HEADERS)
    if response.status_code != 200:
        raise RuntimeError('请求失败')
    with open('四川疫情数据.csv', 'w' , encoding='utf-8-sig') as f:
        f.write('时间,累计确诊,境外输入,累计治愈,死亡,在医院隔离,尚在观察\n')
        Parse(response, f)
        for page in range(2, ALL_PAGE + 1):
            one_page = url1 + str(page) + '.shtml'
            response = requests.get(one_page, headers=HEADERS)
            if response.status_code != 200:
                raise RuntimeError('请求失败')
            Parse(response, f)

if __name__ == '__main__':
    CovidSichuan()