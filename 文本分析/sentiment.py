from aip import AipNlp
from pprint import pprint
import json
import xlrd
import time

""" 你的 APPID AK SK """
APP_ID = '20314748'
API_KEY = '9h90bpYzbzaFPxvgISosLupK'
SECRET_KEY = 'NHg7VIpWnrqQyMgM4nM8lvhViEcGIEBp'
client = AipNlp(APP_ID, API_KEY, SECRET_KEY)  # 涉及个人申请的信息，故不公开


'''
log_id	uint64	请求唯一标识码
prop	string	匹配上的属性词
adj	string	匹配上的描述词
sentiment	int	该情感搭配的极性（0表示消极，1表示中性，2表示积极）
begin_pos	int	该情感搭配在句子中的开始位置
end_pos	int	该情感搭配在句子中的结束位置
abstract	string	对应于该情感搭配的短句摘要
'''

'''
评论观点提取
1 - 酒店
2 - KTV3 - 丽人
4 - 美食餐饮
5 - 旅游
6 - 健康
7 - 教育
8 - 商业
9 - 房产
10 - 汽车
11 - 生活
12 - 购物
13 - 3C
'''

def OpenExcel(filename:str):
    r'C:\Users\12517\Desktop\赛氪\2021年全国大学生数据统计与分析竞赛赛题\题目A\附件1 - 副本.xlsx'
    readbook = xlrd.open_workbook(filename)
    sheet = readbook.sheet_by_name('fj')
    return sheet

def ReadComment(sheet):
    # 从0开始索引
    '''7  13  19'''
    nrows = sheet.nrows
    ncols = sheet.ncols

    comment_dict = {}
    for row in range(nrows):
        if row == 0:
            continue
        one_comment_list = []
        for i in [7, 13, 19]:
            content = sheet.cell(row, i).value.replace('\n', '')
            one_comment_list.append(content)
        comment_dict[str(row)] = one_comment_list
    # content = json.dumps(comment_dict)
    # f = open('评论.json', 'w', encoding='utf8')
    # f.write(content)
    # f.close()
    return comment_dict

def ReadCommentFromJson(jsonfile:str):
    with open(jsonfile, 'r', encoding='utf8') as f:
        comment_dict = f.read()
        comment_dict = json.loads(comment_dict)
    return comment_dict

def BaiduSentiment(comment_dict = None):
    '''使用从百度AI开放平台申请的API，进行文本情感分析，保存为json格式的文件，并返回处理结果的字典'''
    APP_ID = '填写APP_ID'
    API_KEY = '填写API_KEY'
    SECRET_KEY = '填写SECRET_KEY'
    client = AipNlp(APP_ID, API_KEY, SECRET_KEY)  # 根据填写的信息创建client

    if comment_dict == None:
        comment_dict = ReadCommentFromJson(r'评论.json') # 如果没有输入字典，则读取json格式的文件
    keys = comment_dict.keys()
    result_dict = {} # 创建保存结果的字典
    num = 0
    for key in keys:
        num += 1
        one_comment_list = comment_dict[key]
        one_paper_result_list = []
        for i in range(3):
            time.sleep(0.5)
            text = one_comment_list[i]
            if len(text) == 0:
                result = {'confidence': 1.000000, 'negative_prob': 0.5, 'positive_prob': 0.5, 'sentiment': 1}  # 如果没有评论，则自动写入中性的评价
                one_paper_result_list.append(result)
            else:
                result = client.sentimentClassify(text)
                if 'error_code' in result.keys(): # 判断是否出错，如果出错，返回错误的结果，并终止程序运行
                    print(result)
                    return
                one_paper_result_list.append(result['items'])
                print(result)
        result_dict[key] = one_paper_result_list
    result_dict = json.dumps(result_dict)
    with open('result.json', 'w', encoding='utf8') as f: # 保存结果到json文件
        f.write(result_dict)
        return result_dict
def ResultToExcel(out_csv:str, json_file:str):
    with open(json_file, 'r', encoding='utf8') as f:
        content = f.read()
        content_dict = json.loads(content)
        del content
    keys = content_dict.keys()
    '''col from 22'''
    f = open(out_csv, 'w', encoding='utf8')
    for key in keys:
        one_paper_comment_list = content_dict[key]
        one_papaer_comment_outlist = []
        one_papaer_comment_outlist.append(key)
        for one_comment in one_paper_comment_list:
            try:
                one_comment = one_comment[0]
            except:
                pass
            positive = one_comment['positive_prob']
            confidence = one_comment['confidence']
            sentiment = one_comment['sentiment']

            one_papaer_comment_outlist.append(positive)
            one_papaer_comment_outlist.append(confidence)
            one_papaer_comment_outlist.append(sentiment)
        for index, one in enumerate(one_papaer_comment_outlist):
            if index == len(one_papaer_comment_outlist) - 1:
                f.write(str(one) + '\n')
            else:
                f.write(str(one) + ',')
    f.close()

def TenPercentCompute(excel_path:str):
    work_book = xlrd.open_workbook(excel_path)
    sheet = work_book.sheet_by_name('专家观点评价模型')
    '33'
    content = sheet.col_values(32)
    content = content[1:]
    content_sort = sorted(content)
    tenpercent_score = content_sort[int(len(content_sort) * 0.9)]
    out_score_dict = {}
    for index, one_score in enumerate(content):
        if one_score >= tenpercent_score:
            out_score_dict[str(index + 1)] = '优秀'
        else:
            out_score_dict[str(index + 1)] = '不优秀'
    with open('优秀.json', 'w', encoding='utf8') as f:
        out_score_dict_json = json.dumps(out_score_dict)
        f.write(out_score_dict_json)
    keys = out_score_dict.keys()
    f = open('优秀.csv','w', encoding='gbk')
    for index, key in enumerate(keys):
        f.write(key + ',' + out_score_dict[key] + '\n')
    f.close()

if __name__ == '__main__':
    # BaiduSentiment()
    TenPercentCompute(r'C:\Users\12517\Desktop\赛氪\2021年全国大学生数据统计与分析竞赛赛题\题目A\附件1 - 副本.xlsx')
    # ResultToExcel(out_csv=r'C:\Users\12517\Desktop\赛氪\2021年全国大学生数据统计与分析竞赛赛题\题目A\情感分析.csv', json_file=r'C:\Users\12517\Desktop\赛氪\2021年全国大学生数据统计与分析竞赛赛题\题目A\code\情感分析结果.json')