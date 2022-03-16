#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: wild_orange
# @Email: jixuanfan_seu@163.com
# @Date:   2020-07-21 22:20:06
# @Last Modified time: 2020-10-25 19:39:31

import requests
import datetime
import time
import json

headers={'User-Agent': 'Chrome/76.0.3809.132'}
base_url='http://index.baidu.com/'
cookies={'Cookie':'HMACCOUNT=9C5F7785E07A4211; BAIDUID=700EE2C2D0C2D5DF844E083C482655E4:FG=1; BIDUPSID=F3A68ECF30CB7CFA4345C61E12FFA3A4; PSTM=1602203028; BDUSS=lCWXRld1VEfkZJUThnYXB5RkkzQkhvb2FJSlUxSXNIMXVGZmhsNEVBR1BQck5nRVFBQUFBJCQAAAAAAAAAAAEAAACBSeOYxvHUu7K7vKsAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAI-xi2CPsYtgNk; MCITY=-%3A; __yjs_duid=1_5156761f6e5c6b2032ace7ad63ff87581620707791087; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; BA_HECTOR=2g0l8g0g2kaha480f31gcj56e0q; BDRCVFR[Fc9oatPmwxn]=srT4swvGNE6uzdhUL68mv3; delPer=0; PSINO=1; H_PS_PSSID=34099_33969_31253_34004_33607_26350; BCLID=11307570168191751854; BDSFRCVID=BJ_OJeC62RY3ocne18agM0fMbMIPjrrTH6aoVuDrupJYzmPycYKAEG0PEM8g0KA-S2MMogKKXgOTHw0F_2uxOjjg8UtVJeC6EG0Ptf8g0f5; H_BDCLCKID_SF=tRAOoCKKtCvqKRopMtOhq4tehHRGBqR9WDTm_Do4yCOoHnrNDj7HbUrQb4caWxcT2jrH-pPKKR74fqb45J3kWJID0hr2XxnC3mkjbp5zfn02OpDz0T5YXt4syPRvKMRnWTkjKfA-b4ncjRcTehoM3xI8LNj405OTbIFO0KJDJCcjqR8Zj50aDjoP; RT=\"z=1&dm=baidu.com&si=v4rvp5oan0s&ss=kpz1a4ry&sl=1h&tt=1an9&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=16mfc&ul=1ctzv&hd=1cudq\"; ab_sr=1.0.1_OTA3ZDRiNjViNDg3ZjQ2NTcyZTk5ZjQwYzg0ZjUyNWQ4YWY0NWZiNjgyNWM4YTY4ZDIxMWU5ZDQwNzVjNGI0ZDZhNzdjNDdiNTQ0NTY3NWRkMzExM2UzYTU5M2YyZmVhYmU0ZmFmNzk4YmIwZDM1YWU4NjJlY2RiMjA2MDRkYmZkYmE5ZGJjNzA1MTM0ZGQ4MjE1NmUwZTE4ODI0YjIzNzE4YjQzYjRmYzYxNTQyYjk1MDZiNGYyNmY2MDNiNTM4; __yjs_st=2_OTgzNTE1YzcxZGQ3ZWIzYjNlZGZmNDEyN2MwNjkwZTc2ZDdkMDgzMWU3M2JmZDJkNGVhYTI3MDk4N2NjNTFkNjQxNmYxM2RiNTM4ZjIyN2ZhZDUxOTU1MDQyZjRmNWExY2FkMDc3OTQxYTJmNDM4YWE2YzA4YmEzMGVjMDA4OTBmMjgzYTJmNjExZTIzZDM4M2I2Y2ZjYzY4M2ZkODc0N2YzNTllMWJiMzhlMWNhYWUzODFkOTFkMjZmZGYyMzY1MjJlYmM4MDQyZDE5YzQyZGFkZWExZmMyYTUzMDVlYjA3NWNhZGI5NmUyNzQwN2IwODk1OTdmMTUwMzdlOTY4OV83X2Y5MmM1MzU1; bdindexid=gjerk3vu1avs4tlqat9qct7th7; HMVT=6bcd52f51e9b3dce32bec4a3997715ac|1623823417|; ZD_ENTRY=baidu'}
# 加载区域编码文件
index_file='baidu_index_code.csv'
with open(index_file,encoding='utf-8') as f:
	data=[x.strip().split(',') for x in f.readlines()]
	r_codes={x[1]:x[0] for x in data}
	codes={x[0]:x[1] for x in data}

def decrypt(t,e):
	n, i, a, result = list(t), list(e), {}, []
	ln = int(len(n)/2)
	start, end = n[ln:], n[:ln]
	a = dict(zip(end, start))
	return ''.join([a[j] for j in e])

def get_ptbk(uniqid):
	url=base_url+'Interface/ptbk?uniqid=%s'%uniqid
	res=requests.get(url,headers=headers,cookies=cookies)
	if res.status_code==200:
		ptbk=res.json()['data']
		return ptbk
	else:
		print('uniqid获取失败~状态码为：%s'%res.status_code)
		return None

def parse_date(start,end):
	START=datetime.datetime.strptime(start,'%Y-%m-%d')
	END=datetime.datetime.strptime(end,'%Y-%m-%d')
	BEGIN=datetime.datetime.strptime('2011-01-01','%Y-%m-%d') #百度指数能查到的最早日期
	LAST=datetime.datetime.today()-datetime.timedelta(days=1) #百度指数能查到的最晚日期
	if START<BEGIN: START=BEGIN
	if END>LAST: END=LAST
	delta_days=(END-START).days
	if delta_days<0:
		print('开始日期不能晚于结束日期！')
		return None
	START_STR=START.strftime('%Y-%m-%d')

	BATCH=360 #每次提取BATCH天数据，若查询的时间范围超过一年，则百度指数返回以周为周期的数据
	retVal=[]
	curDate=END
	curPreDate=curDate-datetime.timedelta(days=BATCH)
	curPreDate_str=curPreDate.strftime('%Y-%m-%d')
	curDate_str=curDate.strftime('%Y-%m-%d')
	retVal.append([START_STR if curPreDate<START else curPreDate_str,curDate_str])
	curDate=curPreDate-datetime.timedelta(days=1)
	while curDate>START:
		curPreDate=curDate-datetime.timedelta(days=BATCH)
		curPreDate_str=curPreDate.strftime('%Y-%m-%d')
		curDate_str=curDate.strftime('%Y-%m-%d')
		retVal.append([START_STR if curPreDate<START else curPreDate_str,curDate_str])
		curDate=curPreDate-datetime.timedelta(days=1)
	retVal=retVal[::-1] #逆序转换
	return retVal

def ReadCity(path:str):
    with open(path, 'r', encoding='utf8') as f:
        content_list = f.readlines()
       # content_list = content_list[1:len(content_list)]
        for content in content_list:
            content = content.replace('\n', '')
            content = content.split(',')
            yield content[0], content[1]
        

def Baidu_index(keyword,start,end,area='0',fmt='L'):
	'''
		@param:
			keyword: str, 需要查询的词汇
			start：str, 开始时间，'20XX-XX-XX'格式，不能早于2011-01-01
			end：str，结束时间，20XX-XX-XX'格式，不能晚于前一天时间
			area：int/str, 区域编码或者名称，需要提前在baidu_index_code.csv文件中配置（目前已配置全国、省、江苏地级市)
			fmt: 'L'或'D', 返回值格式，分别表示数组格式(List)和字典格式(Dict)。
		@output:
			若fmt为'L'，返回一个二维数组，每一行表示：日期字符串, PC+移动端数据, PC端数据, 移动端数据。按时间先后顺序排序。
			若fmt为'D'，返回一个字典，共有4个key-value：
					period: list, [开始日期字符串，结束日期字符串]
					all: list of int, PC+移动端数据, 按时间先后顺序排序
					pc: list of int, PC端数据, 按时间先后顺序排序
					mobile: list of int, 移动端数据, 按时间先后顺序排序
	'''
	area=str(area)
	if not area.isdigit():  #如果是区域名称（不是编码）
		if area not in r_codes.keys():
			print('区域编码文件中无%s的编码~'%area)
			return None
		else:
			code=r_codes[area]
	else:
		if area not in codes.keys():
			print('区域编码文件中无编码:%s'%area)
			return
		else:
			code=area

	dates=parse_date(start,end)
	if not dates: return None
	all_data=[]     #pc+移动端数据
	pc_data=[]      #pc端数据
	mobile_data=[]  #移动端数据
	for date in dates:
		#print('正在查询%s%s至%s的数据'%(codes[code],date[0],date[1]))
		url=base_url+'api/SearchApi/index?area=%s&word=[[%%7B"name":"%s","wordType":1%%7D]]&startDate=%s&endDate=%s'%(code,keyword,date[0],date[1])
		res=requests.get(url,headers=headers,cookies=cookies)
		if res.status_code==200:
			data=res.json()['data']
			all_val=data['userIndexes'][0]['all']['data']
			pc_val=data['userIndexes'][0]['pc']['data']
			mobile_val=data['userIndexes'][0]['wise']['data']
			uniqid=data['uniqid']
			ptbk=get_ptbk(uniqid)
			all_data+=[int(x) if x else 0 for x in decrypt(ptbk,all_val).split(',')]
			pc_data+=[int(x) if x else 0 for x in decrypt(ptbk,pc_val).split(',')]
			mobile_data+=[int(x) if x else 0 for x in decrypt(ptbk,mobile_val).split(',')]
		else:
			print('数据获取失败~状态码为：%s'%res.status_code)
			return None
		time.sleep(3.5)
	if fmt=='L':
		START=datetime.datetime.strptime(dates[0][0],'%Y-%m-%d')
		END=datetime.datetime.strptime(dates[-1][1],'%Y-%m-%d')
		curDate=START
		all_dates_str=[]
		while curDate<=END:
			all_dates_str.append(curDate.strftime('%Y-%m-%d'))
			curDate+=datetime.timedelta(days=1)
			retVal=list(zip(all_dates_str,all_data,pc_data,mobile_data))
	elif fmt=='D':
		retVal={'period':[dates[0][0],dates[-1][1]],'all':all_data,'pc':pc_data,'mobile':mobile_data}
	else:
		print('fmt参数只能为L或D')
		retVal=None
	return retVal

def License():
	S='87/101/108/99/111/109/101/32/116/111/32/117/115/101/32/116/104/105/115/32/112/114/111/103/\
	114/97/109/33/10/65/117/116/104/111/114/58/32/68/101/99/111/100/101/10/72/111/109/101/112/97/\
	103/101/58/32/71/105/116/101/101/40/104/116/116/112/115/58/47/47/103/105/116/101/101/46/99/111/\
	109/47/106/105/120/117/97/110/102/97/110/41/10/32/32/32/32/32/32/32/32/32/32/67/83/68/78/40/104/\
	116/116/112/115/58/47/47/98/108/111/103/46/99/115/100/110/46/110/101/116/47/113/113/95/51/53/52/\
	48/56/48/51/48/41/10'
	print(''.join([chr(int(x)) for x in S.split('/')]))
License()

if __name__ == '__main__':
	'''START='2020-09-01'
	END='2020-10-01'
	data=Baidu_index('泰山',START,END,'0')
        print(data)'''
a = ReadCity(r'E:\spyder\crawler-api\百度指数\新建文本文档.csv')
file = open(r'E:\spyder\crawler-api\百度指数\123.csv', 'w', encoding='utf_8_sig')
for id, city in a:
    time.sleep(2)
    result = Baidu_index('泰山',start='2011-01-01',end='2021-06-15',area=city)
    for i in result:
        i0 = i[0]
        i1 = i[1]
        i2 = i[2]
        i3 = i[3]
        file.write(city + ',' + i0 + ',' + str(i1) + ',' + str(i2) + ',' + str(i3) + '\n')
file.close()