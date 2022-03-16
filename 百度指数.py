# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 14:16:37 2021

@author: MM
"""

import requests
import sys
import time

word_url = 'http://index.baidu.com/api/SearchApi/thumbnail?area=0&word={}'
COOKIES = ''
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Cookie':'HMACCOUNT=9C5F7785E07A4211; BAIDUID=700EE2C2D0C2D5DF844E083C482655E4:FG=1; BIDUPSID=F3A68ECF30CB7CFA4345C61E12FFA3A4; PSTM=1602203028; BDUSS=lCWXRld1VEfkZJUThnYXB5RkkzQkhvb2FJSlUxSXNIMXVGZmhsNEVBR1BQck5nRVFBQUFBJCQAAAAAAAAAAAEAAACBSeOYxvHUu7K7vKsAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAI-xi2CPsYtgNk; MCITY=-%3A; __yjs_duid=1_5156761f6e5c6b2032ace7ad63ff87581620707791087; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; BA_HECTOR=2g0l8g0g2kaha480f31gcj56e0q; BDRCVFR[Fc9oatPmwxn]=srT4swvGNE6uzdhUL68mv3; delPer=0; PSINO=1; H_PS_PSSID=34099_33969_31253_34004_33607_26350; BCLID=11307570168191751854; BDSFRCVID=BJ_OJeC62RY3ocne18agM0fMbMIPjrrTH6aoVuDrupJYzmPycYKAEG0PEM8g0KA-S2MMogKKXgOTHw0F_2uxOjjg8UtVJeC6EG0Ptf8g0f5; H_BDCLCKID_SF=tRAOoCKKtCvqKRopMtOhq4tehHRGBqR9WDTm_Do4yCOoHnrNDj7HbUrQb4caWxcT2jrH-pPKKR74fqb45J3kWJID0hr2XxnC3mkjbp5zfn02OpDz0T5YXt4syPRvKMRnWTkjKfA-b4ncjRcTehoM3xI8LNj405OTbIFO0KJDJCcjqR8Zj50aDjoP; RT=\"z=1&dm=baidu.com&si=v4rvp5oan0s&ss=kpz1a4ry&sl=1h&tt=1an9&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=16mfc&ul=1ctzv&hd=1cudq\"; ab_sr=1.0.1_OTA3ZDRiNjViNDg3ZjQ2NTcyZTk5ZjQwYzg0ZjUyNWQ4YWY0NWZiNjgyNWM4YTY4ZDIxMWU5ZDQwNzVjNGI0ZDZhNzdjNDdiNTQ0NTY3NWRkMzExM2UzYTU5M2YyZmVhYmU0ZmFmNzk4YmIwZDM1YWU4NjJlY2RiMjA2MDRkYmZkYmE5ZGJjNzA1MTM0ZGQ4MjE1NmUwZTE4ODI0YjIzNzE4YjQzYjRmYzYxNTQyYjk1MDZiNGYyNmY2MDNiNTM4; __yjs_st=2_OTgzNTE1YzcxZGQ3ZWIzYjNlZGZmNDEyN2MwNjkwZTc2ZDdkMDgzMWU3M2JmZDJkNGVhYTI3MDk4N2NjNTFkNjQxNmYxM2RiNTM4ZjIyN2ZhZDUxOTU1MDQyZjRmNWExY2FkMDc3OTQxYTJmNDM4YWE2YzA4YmEzMGVjMDA4OTBmMjgzYTJmNjExZTIzZDM4M2I2Y2ZjYzY4M2ZkODc0N2YzNTllMWJiMzhlMWNhYWUzODFkOTFkMjZmZGYyMzY1MjJlYmM4MDQyZDE5YzQyZGFkZWExZmMyYTUzMDVlYjA3NWNhZGI5NmUyNzQwN2IwODk1OTdmMTUwMzdlOTY4OV83X2Y5MmM1MzU1; bdindexid=gjerk3vu1avs4tlqat9qct7th7; HMVT=6bcd52f51e9b3dce32bec4a3997715ac|1623823417|; ZD_ENTRY=baidu',
    'DNT': '1',
    'Host': 'index.baidu.com',
    'Pragma': 'no-cache',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://index.baidu.com/v2/main/index.html',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}


def decrypt(t,e):
    n = list(t)
    i = list(e)
    a = {}
    result = []
    ln = int(len(n)/2)
    start = n[ln:]
    end = n[:ln]
    for j,k in zip(start, end):
        a.update({k: j})
    for j in e:
        result.append(a.get(j))
    return ''.join(result)
    

def get_ptbk(uniqid):
    url = 'http://index.baidu.com/Interface/ptbk?uniqid={}'
    resp = requests.get(url.format(uniqid), headers=headers)
    if resp.status_code != 200:
        print('获取uniqid失败')
        sys.exit(1)
    return resp.json().get('data')
    

def get_index_data(keyword, start='2011-01-03', end='2021-06-15'):
    keyword = str(keyword).replace("'", '"')
    url = f'http://index.baidu.com/api/SearchApi/index?area=0&word={keyword}&area=0&startDate={start}&endDate={end}'

    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        print('获取指数失败')
        sys.exit(1)

    content = resp.json()
    data = content.get('data')
    user_indexes = data.get('userIndexes')[0]
    uniqid = data.get('uniqid')
    ptbk = get_ptbk(uniqid)

    while ptbk is None or ptbk == '':
        ptbk = get_ptbk(uniqid)

    all_data = user_indexes.get('all').get('data')
    result = decrypt(ptbk, all_data)
    result = result.split(',')

    with open('百度指数4.csv', 'w', encoding='utf8') as f:
        for i in result:
            f.write(i + '\n')
            print('百度指数:%s' % i)
    

if __name__ == '__main__':
    words = [[{"name": "泰山+", "wordType": 1}]]
    get_index_data(words)

