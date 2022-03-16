from bs4 import BeautifulSoup
import pandas as pd
import json
import requests
import time

def get_static_url_content(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    req = requests.get(url, headers=headers)
    content = req.text
    bsObj = BeautifulSoup(content, 'lxml')#jiexi
    return bsObj

def get_jd_comment(url):
    # 该景点最大评论数
    maxnum = get_static_url_content(url).find('span', {'class': 'e_nav_comet_num'}).text
    maxnum = int(maxnum) # 得到所有的页数

    poi = ''.join([x for x in url if x.isdigit()])  #取出其中的poi数字

    cat_user_id = []
    cat_user_name= []
    cat_jd_poi = []
    cat_score = []
    cat_user_comment = []
    cat_comment_time = []

    url = 'http://travel.qunar.com/place/api/html/comments/poi/' + poi + '?poiList=true&sortField=1&rank=0&pageSize=50&page='
    '''http://travel.qunar.com/place/api/comments/5939065/replies?page=1&pageSize=10&format=json
       http://travel.qunar.com/place/api/html/comments/poi/709762?poiList=true&sortField=1&rank=0&pageSize=50&page=1'
    '''

    #这里页数暂时设为101,取的pageSize=50,即爬取100*50条评论
    page = 101
    if (page - 1) * 50 > maxnum:
        page = int(((maxnum + 50) / 50)+1)

    for i in range(1, page):
        """开始每一页的爬虫"""
        url1 = url + str(i)
        json_str = requests.get(url1, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}).text

        json_data=json.loads(json_str)['data']
        #print(json_data)
        bsObj = BeautifulSoup(json_data, 'lxml')
        bs=bsObj.find_all('li',{'class':'e_comment_item clrfix'})

        for j in range(0,len(bs)):
            try:
                user=bs[j].find('div', {'class': 'e_comment_usr_name'}).find('a')
                cat_user_id.append(''.join([x for x in user.attrs['href'] if x.isdigit()]))

                cat_user_name.append(user.text)

                cat_jd_poi.append(poi)

                score=''.join([x for x in str(bs[j].find('span',{'class':'total_star'}).find('span')) if x.isdigit()])
                cat_score.append(score)

                a=bs[j].find('div',{'class':'e_comment_content'}).find_all('p')
                cat_user_comment.append(''.join(x.text for x in a))

                cat_comment_time.append(bs[j].find('div',{'class':'e_comment_add_info'}).find('li').text)

            except:
                print('i=',i,'j=',j,'有问题')
        print('已完成poi=',poi,' ',i,'/',page-1)
        print(cat_user_comment)
        time.sleep(0.2)

    return cat_user_id,cat_user_name,cat_jd_poi,cat_score,cat_comment_time,cat_user_comment


url = 'http://travel.qunar.com/p-oi709762-mogaoku'

cat_user_id, \
cat_user_name, \
cat_jd_poi, \
cat_score, \
cat_comment_time, \
cat_user_comment\
    = get_jd_comment(url)

city=pd.DataFrame({'user_id':cat_user_id,
                   'user_name':cat_user_name,
                   'jd_poi':cat_jd_poi,
                   'score':cat_score,
                   'time':cat_comment_time,
                   'comment':cat_user_comment})
city.to_csv('mokaoku-jd-comment.csv', encoding='utf_8_sig')
