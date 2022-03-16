import requests
from lxml import etree
import re
import time

'''
字典键解析：
address ：地址
belong ： 四川省
city_name, county_name
level_name ： 普通本科
duan_class_name ： 双一流
nature_name :公办
name ： 学校名字
rank ： 排名
school_id ： 学校id
'''

URL_PARTERN = 'https://api.eol.cn/gkcx/api/?access_token=&admissions=&central=&department=&dual_class=&f211=&f985=&is_doublehigh=&is_dual_class=&keyword=&nature=&page=%d&province_id=&ranktype=&request_type=1&school_type=&signsafe=&size=20&sort=view_total&top_school_id=[661,100,264,270,769,770,822,2502,771,3193,3186,659,1084]&type=&uri=apidata/api/gk/school/lists'
PAGES = 143
headers = {
    'Origin': 'https://gkcx.eol.cn',
    'Referer': 'https://gkcx.eol.cn/',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json;charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36'
}

def GaokaoSchool():
    with open('大学名称.csv', 'w', encoding='gbk') as f:
        for page in range(1, PAGES + 1):
            url = URL_PARTERN % page
            response = requests.get(url, headers=headers)
            result = response.text
            result = eval(result)
            result = result['data']['item'] # 一个list格式，含有字典，字典保存的是每个大学的信息
            time.sleep(1)
            '''
            字典键解析：
            address ：地址
            belong ： 四川省
            city_name, county_name
            level_name ： 普通本科
            dual_class_name ： 双一流
            nature_name :公办
            name ： 学校名字
            rank ： 排名
            school_id ： 学校id
            '''
            f.write('学校编号' + ',' + '学校名称' + ',' + '排名' + '学校评级' + '学校等级' + ',' + '学校归属' + '是否公办' + '地址')
            for item in result:
                address = item['address']
                belong = item['belong']
                level_name = item['level_name']
                dual_class_name = item['dual_class_name']
                nature_name = item['nature_name']
                name = item['name']
                rank = str(item['rank'])
                school_id = str(item['school_id'])
                print(school_id,name, rank, dual_class_name, level_name, belong, nature_name, address)
                f.write(school_id + ',' + name + ',' + rank + ',' + dual_class_name + ',' + level_name + ',' + belong + ',' + nature_name + ',' + address + '\n')

if __name__ == '__main__':
    GaokaoSchool()